from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_verified', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_staff', 'date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'is_verified')}),
    )
    actions = ['verify_counselors', 'unverify_counselors']
    
    def verify_counselors(self, request, queryset):
        """Verify selected counselors"""
        queryset.filter(role='counselor').update(is_verified=True)
        self.message_user(request, f"{queryset.filter(role='counselor').count()} counselors verified.")
    verify_counselors.short_description = "Verify selected counselors"
    
    def unverify_counselors(self, request, queryset):
        """Unverify selected counselors"""
        queryset.filter(role='counselor').update(is_verified=False)
        self.message_user(request, f"{queryset.filter(role='counselor').count()} counselors unverified.")
    unverify_counselors.short_description = "Unverify selected counselors"

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'created_at', 'updated_at']
    readonly_fields = ['session_id', 'created_at', 'updated_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_preview', 'timestamp', 'sentiment_score']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_date', 'counselor', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'counselor']
    search_fields = ['reason']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'language', 'created_at']
    list_filter = ['type', 'language', 'created_at']
    search_fields = ['title', 'description']

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ['title', 'moderated', 'replies_count', 'likes_count', 'shares_count', 'timestamp']
    list_filter = ['moderated', 'timestamp']
    search_fields = ['title', 'content']

@admin.register(ForumPostLike)
class ForumPostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'session', 'timestamp']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']

@admin.register(ForumPostShare)
class ForumPostShareAdmin(admin.ModelAdmin):
    list_display = ['post', 'session', 'share_platform', 'timestamp']
    list_filter = ['share_platform', 'timestamp']
    readonly_fields = ['timestamp']

=======
    list_display = ['title', 'moderated', 'replies_count', 'timestamp']
    list_filter = ['moderated', 'timestamp']
    search_fields = ['title', 'content']

>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ['post', 'content_preview', 'moderated', 'timestamp']
    list_filter = ['moderated', 'timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_sessions', 'anxiety_keywords', 'depression_keywords', 'appointments_booked']
    list_filter = ['date']
    readonly_fields = ['date']
