from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist'

    def handle(self, *args, **kwargs):
        username = "admin" # আপনার ইউজারনেম
        password = "yourpassword" # আপনার পছন্দমতো পাসওয়ার্ড
        email = "admin@example.com"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists'))