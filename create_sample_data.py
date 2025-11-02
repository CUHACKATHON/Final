#!/usr/bin/env python
"""
Script to create sample data for testing
Run: python create_sample_data.py
"""

import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentalhealth.settings')
django.setup()

from core.models import CustomUser, Resource, ChatSession, ForumPost, Analytics
from django.contrib.auth import get_user_model
from datetime import date

def create_sample_data():
    print("Creating sample data...")
    
    # Create sample counselors if they don't exist
    if not CustomUser.objects.filter(username='counselor1').exists():
        counselor1 = CustomUser.objects.create_user(
            username='counselor1',
            password='demo123',
<<<<<<< HEAD
            email='counselor1@moodlift.com',
=======
            email='counselor1@mindcare.com',
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
            role='counselor',
            first_name='Dr. Priya',
            last_name='Sharma'
        )
        print(f"Created counselor: {counselor1.username}")
    else:
        counselor1 = CustomUser.objects.get(username='counselor1')
    
    if not CustomUser.objects.filter(username='counselor2').exists():
        counselor2 = CustomUser.objects.create_user(
            username='counselor2',
            password='demo123',
<<<<<<< HEAD
            email='counselor2@moodlift.com',
=======
            email='counselor2@mindcare.com',
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
            role='counselor',
            first_name='Dr. Raj',
            last_name='Kumar'
        )
        print(f"Created counselor: {counselor2.username}")
    else:
        counselor2 = CustomUser.objects.get(username='counselor2')
    
    # Create sample resources
    resources_data = [
        {
            'title': 'Managing Exam Stress - English',
            'description': 'A comprehensive guide to managing stress during exam season with evidence-based techniques.',
            'type': 'video',
            'file_path': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Replace with actual video URL
            'language': 'en'
        },
        {
            'title': 'Guided Meditation for Anxiety - Hindi',
            'description': 'A 15-minute guided meditation specifically designed for anxiety relief.',
            'type': 'meditation',
            'file_path': '/static/assets/meditation_anxiety_hindi.mp3',
            'language': 'hi'
        },
        {
            'title': 'Understanding Depression - Article',
            'description': 'An informative article about recognizing and managing depression symptoms.',
            'type': 'article',
            'file_path': '/static/assets/depression_article.pdf',
            'language': 'en'
        },
        {
            'title': 'Sleep Hygiene Tips - Tamil',
            'description': 'Practical tips for improving sleep quality during stressful periods.',
            'type': 'article',
            'file_path': '/static/assets/sleep_tips_tamil.pdf',
            'language': 'ta'
        },
    ]
    
    for res_data in resources_data:
        if not Resource.objects.filter(title=res_data['title']).exists():
            Resource.objects.create(**res_data)
            print(f"Created resource: {res_data['title']}")
    
    # Create sample forum post (will need moderation)
    if not ForumPost.objects.filter(title='Feeling overwhelmed with studies').exists():
        session = ChatSession.objects.create()
        ForumPost.objects.create(
            session=session,
            title='Feeling overwhelmed with studies',
            content='I\'m a second-year engineering student and the pressure is really getting to me. Any advice?',
            moderated=False
        )
        print("Created sample forum post (pending moderation)")
    
    # Create sample analytics for last 7 days
    today = date.today()
    for i in range(7):
        day = today - timedelta(days=i)
        analytics, created = Analytics.objects.get_or_create(date=day)
        if created:
            analytics.total_sessions = i * 3 + 5
            analytics.anxiety_keywords = i * 2
            analytics.depression_keywords = i + 1
            analytics.appointments_booked = i
            analytics.save()
            print(f"Created analytics for {day}")
    
    print("\nSample data created successfully!")
    print("\nLogin credentials:")
    print("  Admin: Use your superuser credentials")
    print("  Counselor 1: username='counselor1', password='demo123'")
    print("  Counselor 2: username='counselor2', password='demo123'")
    print("\nNote: Forum posts need to be moderated in the admin panel or dashboard.")

if __name__ == '__main__':
    create_sample_data()

