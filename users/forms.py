from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Profile
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk: # Editing existing user
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
        else: # Creating new user
            self.fields['password'].required = True

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance.pk and not password: # Se for um novo usuário e a senha estiver vazia
            raise ValidationError("A senha é obrigatória para novos usuários.")
        return password

    def save(self, commit=True):
        user = None
        profile = self.instance # A instância de Profile que o formulário está manipulando

        if profile.pk: # Editando um usuário existente
            user = profile.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.is_active = self.cleaned_data['is_active']
            user.save()
            if commit:
                profile.save() # Salva a instância de Profile (que já está ligada ao User)
        else: # Criando um novo usuário
            password = self.cleaned_data.get('password')
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=password,
                is_active=self.cleaned_data['is_active']
            )
            # O signal `create_user_profile` já criou o Profile para este novo usuário.
            # Precisamos obter essa instância de Profile e atualizá-la.
            profile = user.profile # Obtém o Profile criado pelo signal
            profile.user_type = 'producer' # Define o user_type para o novo Profile
            # is_active já foi definido no User, e o signal sincroniza isso.
            if commit:
                profile.save() # Salva o Profile criado pelo signal
            self.instance = profile # Atualiza a instância do formulário para ser o Profile criado pelo signal

        return profile
