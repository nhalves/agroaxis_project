
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

class Command(BaseCommand):
    help = 'Cria perfis para usuários que ainda não os possuem.'

    def handle(self, *args, **options):
        users_sem_perfil = User.objects.filter(profile__isnull=True)
        if not users_sem_perfil.exists():
            self.stdout.write(self.style.SUCCESS('Todos os usuários já possuem um perfil.'))
            return

        for user in users_sem_perfil:
            Profile.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Perfil criado para o usuário: {user.username}'))

        self.stdout.write(self.style.SUCCESS('Verificação de perfis concluída.'))
