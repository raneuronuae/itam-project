from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Force reset password for a specific user'

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            # আপনার ইউজারনেম নিশ্চিত করুন
            user = User.objects.get(username='Ruhul_Amin')
            user.set_password('adminuae')
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Password for {user.username} successfully set to adminuae"))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("User does not exist"))