from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Profile
from .forms import UserProfileForm

def custom_logout(request):
    auth_logout(request)
    messages.success(request, 'Você saiu com segurança. Volte sempre!')
    return redirect('login')

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.user_type == 'admin'

@login_required
@user_passes_test(is_admin)
def producer_list(request):
    producers = Profile.objects.filter(user_type='producer')
    return render(request, 'users/producer_list.html', {'producers': producers})

@login_required
@user_passes_test(is_admin)
def producer_create(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_type = 'producer' # Garante que o tipo seja produtor
            profile.save()
            messages.success(request, 'Produtor cadastrado com sucesso!')
            return redirect('users:producer_list')
        else:
            messages.error(request, 'Erro ao cadastrar produtor. Verifique os dados.')
    else:
        form = UserProfileForm()
    return render(request, 'users/producer_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def producer_update(request, pk):
    profile = get_object_or_404(Profile, pk=pk, user_type='producer')
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produtor atualizado com sucesso!')
            return redirect('users:producer_list')
        else:
            messages.error(request, 'Erro ao atualizar produtor. Verifique os dados.')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/producer_form.html', {'form': form, 'profile': profile})

@login_required
@user_passes_test(is_admin)
def impersonate_producer(request, pk):
    producer_profile = get_object_or_404(Profile, pk=pk, user_type='producer')
    user_to_impersonate = producer_profile.user
    auth_login(request, user_to_impersonate) # Loga o administrador como o produtor
    messages.info(request, f'Você está logado como {user_to_impersonate.username}.')
    return redirect('dashboard') # Redireciona para o dashboard do produtor

@login_required
@user_passes_test(is_admin)
def toggle_producer_status(request, pk):
    profile = get_object_or_404(Profile, pk=pk, user_type='producer')
    user = profile.user
    if user.is_active:
        user.is_active = False
        messages.info(request, f'Produtor {user.username} desativado com sucesso.')
    else:
        user.is_active = True
        messages.success(request, f'Produtor {user.username} ativado com sucesso.')
    user.save()
    return redirect('users:producer_list')
