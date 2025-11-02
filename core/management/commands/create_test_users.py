"""
Management command to create test users for testing
Usage: python manage.py create_test_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates test users (admin, counselor, regular user) for testing'

    def handle(self, *args, **options):
        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
<<<<<<< HEAD
                'email': 'admin@moodlift.com',
=======
                'email': 'admin@mindcare.com',
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: username=admin, password=admin123'))
        else:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Updated admin user password to: admin123'))

        # Create verified counselor
        counselor1, created = User.objects.get_or_create(
            username='counselor1',
            defaults={
<<<<<<< HEAD
                'email': 'counselor1@moodlift.com',
=======
                'email': 'counselor1@mindcare.com',
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
                'role': 'counselor',
                'first_name': 'Dr. Priya',
                'last_name': 'Sharma',
                'is_verified': True
            }
        )
        if created:
            counselor1.set_password('counselor123')
            counselor1.save()
            self.stdout.write(self.style.SUCCESS(f'Created verified counselor: username=counselor1, password=counselor123'))
        else:
            counselor1.set_password('counselor123')
            counselor1.is_verified = True
            counselor1.save()
            self.stdout.write(self.style.SUCCESS(f'Updated counselor1 password and verified status'))

        # Create unverified counselor
        counselor2, created = User.objects.get_or_create(
            username='counselor2',
            defaults={
<<<<<<< HEAD
                'email': 'counselor2@moodlift.com',
=======
                'email': 'counselor2@mindcare.com',
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
                'role': 'counselor',
                'first_name': 'Dr. Raj',
                'last_name': 'Kumar',
                'is_verified': False
            }
        )
        if created:
            counselor2.set_password('counselor123')
            counselor2.save()
            self.stdout.write(self.style.SUCCESS(f'Created unverified counselor: username=counselor2, password=counselor123'))
        else:
            counselor2.set_password('counselor123')
            counselor2.is_verified = False
            counselor2.save()
            self.stdout.write(self.style.SUCCESS(f'Updated counselor2 password'))

        # Create regular user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
<<<<<<< HEAD
                'email': 'testuser@moodlift.com',
=======
                'email': 'testuser@mindcare.com',
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
                'role': 'user',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('user123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created regular user: username=testuser, password=user123'))
        else:
            user.set_password('user123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Updated testuser password'))

        self.stdout.write(self.style.SUCCESS('\nTest users created/updated successfully!'))
        self.stdout.write(self.style.WARNING('\nTest Credentials:'))
        self.stdout.write('  Admin: username=admin, password=admin123')
        self.stdout.write('  Verified Counselor: username=counselor1, password=counselor123')
        self.stdout.write('  Unverified Counselor: username=counselor2, password=counselor123')
        self.stdout.write('  Regular User: username=testuser, password=user123')

