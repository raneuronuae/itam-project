from django.apps import AppConfig

class CoreAssetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_assets'

    def ready(self):
        import core_assets.signals  # এই লাইনটি আপনার signals.py কে সক্রিয় করবে

    # নতুন সুপারইউজার তৈরির কোড
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'password123')