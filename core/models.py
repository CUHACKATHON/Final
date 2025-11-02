from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class CustomUser(AbstractUser):
    """Custom user model for users, counselors, and admins"""
    ROLE_CHOICES = [
        ('user', 'Regular User'),
        ('counselor', 'Counselor'),
        ('admin', 'Administrator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False, help_text="For counselors: verified by admin")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class ChatSession(models.Model):
    """Track anonymous chat sessions"""
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id}"


class ChatMessage(models.Model):
    """Store chat interactions"""
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sentiment_score = models.FloatField(null=True, blank=True, help_text="Sentiment analysis score (-1 to 1)")

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.session.session_id} at {self.timestamp}"


class Appointment(models.Model):
    """Counselor appointments"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    session = models.ForeignKey(ChatSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    counselor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'counselor'})
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, help_text="Optional reason for appointment")
    notes = models.TextField(blank=True, help_text="Counselor notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date']

    def __str__(self):
        return f"Appointment with {self.counselor.username} on {self.appointment_date}"


class Resource(models.Model):
    """Educational content - videos, meditations, articles"""
    TYPE_CHOICES = [
        ('video', 'Video'),
        ('meditation', 'Meditation'),
        ('article', 'Article'),
    ]
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('ta', 'Tamil'),
        ('te', 'Telugu'),
        ('kn', 'Kannada'),
        ('mr', 'Marathi'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file_path = models.CharField(max_length=500, help_text="Path to video/audio file or article content")
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"


class ForumPost(models.Model):
    """Anonymous peer support posts"""
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='forum_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)
    replies_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.title} (Moderated: {self.moderated})"
    
    def get_likes_count(self):
        """Get the actual count of likes"""
        return ForumPostLike.objects.filter(post=self).count()
    
    def update_likes_count(self):
        """Update the cached likes count"""
        self.likes_count = self.get_likes_count()
        self.save(update_fields=['likes_count'])


class ForumReply(models.Model):
    """Replies to forum posts"""
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='forum_replies')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Reply to {self.post.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Update replies count when reply is created or moderated status changes
        if is_new or 'moderated' in kwargs.get('update_fields', []):
            self.post.replies_count = ForumReply.objects.filter(post=self.post, moderated=True).count()
            self.post.save(update_fields=['replies_count'])


class ForumPostLike(models.Model):
    """Anonymous likes on forum posts - tracked by session"""
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='likes')
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='forum_post_likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'session')  # One like per session per post
        ordering = ['-timestamp']

    def __str__(self):
        return f"Like on {self.post.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update post likes count
        self.post.update_likes_count()

    def delete(self, *args, **kwargs):
        post = self.post
        super().delete(*args, **kwargs)
        # Update post likes count after deletion
        post.update_likes_count()


class ForumPostShare(models.Model):
    """Track shares of forum posts"""
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='shares')
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='forum_post_shares')
    share_platform = models.CharField(max_length=50, blank=True, help_text="Platform where shared (optional)")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Share of {self.post.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Update post shares count
            self.post.shares_count = ForumPostShare.objects.filter(post=self.post).count()
            self.post.save(update_fields=['shares_count'])


class Analytics(models.Model):
    """Aggregated statistics for dashboard"""
    date = models.DateField(unique=True, default=timezone.now)
    total_sessions = models.IntegerField(default=0)
    anxiety_keywords = models.IntegerField(default=0)
    depression_keywords = models.IntegerField(default=0)
    appointments_booked = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Analytics'

    def __str__(self):
        return f"Analytics for {self.date}"
