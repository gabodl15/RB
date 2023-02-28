from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, User

@receiver(post_migrate)
def create_root(sender, **kwargs):
    if sender.name == 'users':
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(username='root', password='root')

