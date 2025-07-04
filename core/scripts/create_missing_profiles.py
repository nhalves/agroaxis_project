from django.contrib.auth.models import User
from users.models import Profile

def run():
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)
    print("Perfis de usuário ausentes criados com sucesso.")
