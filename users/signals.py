from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=Profile)
def sync_user_staff_status(sender, instance, created, **kwargs):
    """
    Sincroniza o status `is_staff` do User com o `user_type` do Profile.
    Se o user_type for 'admin', o usuário se torna um staff member.
    Caso contrário, ele não é um staff member.
    """
    user = instance.user
    if instance.user_type == 'admin':
        if not user.is_staff:
            user.is_staff = True
            user.save()
    else:
        if user.is_staff:
            user.is_staff = False
            user.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Cria um Profile padrão para um novo usuário, caso não seja criado via admin.
    O user_type padrão será 'producer'.
    """
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance, user_type='producer')