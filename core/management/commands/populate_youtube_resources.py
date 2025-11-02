"""
Management command to populate YouTube resources categorized by mental health topics
Usage: python manage.py populate_youtube_resources
"""
from django.core.management.base import BaseCommand
from core.models import Resource


class Command(BaseCommand):
    help = 'Populates YouTube resources categorized by mental health topics'

    def handle(self, *args, **options):
        # Define YouTube resources by category
        youtube_resources = [
            # Anxiety Management - English
            {
                'title': 'Understanding and Managing Anxiety',
                'description': 'Learn about anxiety symptoms, causes, and effective coping strategies including breathing exercises and cognitive techniques.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/whpJ7YDKAXY',
                'language': 'en'
            },
            {
                'title': '5-4-3-2-1 Grounding Technique for Anxiety',
                'description': 'Practical grounding exercise to help manage anxiety attacks and panic. Uses the 5 senses technique.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/30VMIEmA114',
                'language': 'en'
            },
            {
                'title': 'Breathing Exercises for Anxiety Relief',
                'description': 'Simple breathing techniques to calm your nervous system and reduce anxiety symptoms.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/tEmt1Znux58',
                'language': 'en'
            },
            # Anxiety Management - Hindi
            {
                'title': 'Anxiety Ko Kaise Manage Karein',
                'description': 'Anxiety ke lakshan, kaaran aur upay. Hindi mein anxiety management ke tips aur techniques.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/Vc1_yfQbc8c',
                'language': 'hi'
            },
            
            # Depression - English
            {
                'title': 'Understanding Depression',
                'description': 'Comprehensive guide to understanding depression, its symptoms, and treatment options. Stigma reduction and support.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/fWFuQR_Wt4M',
                'language': 'en'
            },
            {
                'title': 'Coping with Depression: Practical Strategies',
                'description': 'Evidence-based techniques for managing depression including behavioral activation and cognitive restructuring.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/F2hc2FLOdhI',
                'language': 'en'
            },
            {
                'title': 'How to Support Someone with Depression',
                'description': 'Learn how to help friends or family members dealing with depression. Communication tips and support strategies.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/YgmPI9Rb28Y',
                'language': 'en'
            },
            # Depression - Hindi
            {
                'title': 'Depression Kya Hai Aur Kaise Deal Karein',
                'description': 'Depression ke lakshan, kaaran aur upchar. Hindi mein depression management aur self-help strategies.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/8mE1Xy42H-8',
                'language': 'hi'
            },
            
            # Stress Management - English
            {
                'title': 'Stress Management Techniques for Students',
                'description': 'Practical stress management strategies specifically tailored for college students. Academic and personal stress relief.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/0fL-pn80s-c',
                'language': 'en'
            },
            {
                'title': 'Progressive Muscle Relaxation for Stress',
                'description': 'Guided progressive muscle relaxation technique to release physical tension and reduce stress.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/1nZEdq7dG70',
                'language': 'en'
            },
            {
                'title': 'Managing Exam Stress and Academic Pressure',
                'description': 'Tips for dealing with exam anxiety, study stress, and academic pressure. Time management and self-care strategies.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/C3ykSZQeLdM',
                'language': 'en'
            },
            # Stress Management - Hindi
            {
                'title': 'Students Ke Liye Stress Management',
                'description': 'College students ke liye stress management techniques. Exam stress aur academic pressure kaise handle karein.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/Pf1xDt8tE9k',
                'language': 'hi'
            },
            
            # Meditation & Mindfulness - English
            {
                'title': '10 Minute Guided Meditation for Beginners',
                'description': 'Easy-to-follow 10-minute meditation session perfect for beginners. Learn mindfulness and relaxation techniques.',
                'type': 'meditation',
                'file_path': 'https://www.youtube.com/embed/inpok4MKdLM',
                'language': 'en'
            },
            {
                'title': 'Mindfulness Meditation for Anxiety and Stress',
                'description': 'Mindfulness practice specifically designed to help with anxiety and stress. Learn to observe thoughts without judgment.',
                'type': 'meditation',
                'file_path': 'https://www.youtube.com/embed/SEfs5TJZ6Nk',
                'language': 'en'
            },
            {
                'title': 'Body Scan Meditation for Deep Relaxation',
                'description': 'Guided body scan meditation to release tension and promote deep relaxation throughout your body.',
                'type': 'meditation',
                'file_path': 'https://www.youtube.com/embed/qzMQzaOPBec',
                'language': 'en'
            },
            # Meditation & Mindfulness - Hindi
            {
                'title': 'Anxiety Aur Stress Ke Liye Meditation',
                'description': 'Hindi mein guided meditation. Anxiety aur stress ko kam karne ke liye mindfulness practice.',
                'type': 'meditation',
                'file_path': 'https://www.youtube.com/embed/z6X5oEIg6Ak',
                'language': 'hi'
            },
            {
                'title': 'Shavasana - Relaxation Meditation in Hindi',
                'description': 'Shavasana meditation Hindi mein. Deep relaxation aur peace ke liye guided practice.',
                'type': 'meditation',
                'file_path': 'https://www.youtube.com/embed/INJ0bhZ1VP8',
                'language': 'hi'
            },
            
            # Sleep & Insomnia - English
            {
                'title': 'Sleep Hygiene: Tips for Better Sleep',
                'description': 'Learn about sleep hygiene practices, how to improve sleep quality, and manage insomnia naturally.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/_xQ-_VXZsk4',
                'language': 'en'
            },
            {
                'title': 'Guided Sleep Meditation for Insomnia',
                'description': 'Relaxing guided meditation to help you fall asleep faster and improve sleep quality. Natural sleep aid.',
                'type': 'meditation',
                'file_path': 'https://www.youtube.com/embed/r2S5tfnQx6E',
                'language': 'en'
            },
            
            # Self-Care & Wellness - English
            {
                'title': 'Self-Care for Mental Health',
                'description': 'Importance of self-care for mental wellbeing. Practical self-care activities and routines you can start today.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/sQuaFLjagbc',
                'language': 'en'
            },
            {
                'title': 'Building Emotional Resilience',
                'description': 'Learn how to build emotional resilience and bounce back from challenges. Coping skills and mental strength.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/Nq5A-C0t-5I',
                'language': 'en'
            },
            
            # Relationship & Social - English
            {
                'title': 'Dealing with Loneliness and Social Isolation',
                'description': 'Understanding loneliness, its impact on mental health, and practical ways to build connections and reduce isolation.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/FFrNRHbbOK4',
                'language': 'en'
            },
            {
                'title': 'Building Healthy Relationships',
                'description': 'Tips for building and maintaining healthy relationships. Communication skills and boundary setting.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/XfqOB4DVvlE',
                'language': 'en'
            },
            
            # Study & Academic Success - English
            {
                'title': 'Managing Academic Pressure and Burnout',
                'description': 'Strategies for managing academic workload, preventing burnout, and maintaining work-life balance as a student.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/FzVR_xymBdg',
                'language': 'en'
            },
            {
                'title': 'Time Management for Students',
                'description': 'Effective time management techniques for students. Balance academics, self-care, and social life.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/arj7oStGLkU',
                'language': 'en'
            },
            
            # Crisis & Suicide Prevention - English
            {
                'title': 'Mental Health Crisis: How to Get Help',
                'description': 'Information about mental health crisis resources, hotlines, and when to seek immediate professional help.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/HKb5TZ1OrvU',
                'language': 'en'
            },
            {
                'title': 'Suicide Prevention: You Are Not Alone',
                'description': 'Important message about suicide prevention, warning signs, and how to help yourself or someone you know.',
                'type': 'video',
                'file_path': 'https://www.youtube.com/embed/eGltYomfWZ8',
                'language': 'en'
            },
        ]

        created_count = 0
        updated_count = 0

        for resource_data in youtube_resources:
            resource, created = Resource.objects.get_or_create(
                title=resource_data['title'],
                defaults=resource_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'[+] Created: {resource_data["title"]} ({resource_data["language"]})'
                    )
                )
            else:
                # Update existing resource
                for key, value in resource_data.items():
                    setattr(resource, key, value)
                resource.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'[~] Updated: {resource_data["title"]} ({resource_data["language"]})'
                    )
                )

        self.stdout.write(self.style.SUCCESS(
            f'\n[SUCCESS] Successfully populated YouTube resources!'
        ))
        self.stdout.write(f'  Created: {created_count} new resources')
        self.stdout.write(f'  Updated: {updated_count} existing resources')
        self.stdout.write(f'  Total: {Resource.objects.count()} resources in database')

