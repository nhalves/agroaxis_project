from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrador'),
        ('producer', 'Produtor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.get_user_type_display()}'