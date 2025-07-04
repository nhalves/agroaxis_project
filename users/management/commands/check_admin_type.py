
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Verifica o tipo de perfil do usuário admin.'

    def handle(self, *args, **options):
        try:
            admin_user = User.objects.get(username='admin')
            if hasattr(admin_user, 'profile'):
                self.stdout.write(self.style.SUCCESS(f'O tipo de perfil do admin é: {admin_user.profile.user_type}'))
            else:
                self.stdout.write(self.style.WARNING('O usuário admin não possui um perfil associado.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Usuário "admin" não encontrado.'))
