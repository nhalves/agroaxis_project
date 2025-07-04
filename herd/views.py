from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from users.views import is_admin # Importa a função is_admin
from .models import Animal, ReproductiveEvent, HealthEvent
from .forms import AnimalForm, ReproductiveEventForm, HealthEventForm
from .filters import AnimalFilter
from users.models import Profile

@login_required
def animal_list(request):
    """Exibe a lista de animais cadastrados com filtros e paginação."""
    queryset = Animal.objects.all().order_by('name')

    if not request.user.is_staff:
        queryset = queryset.filter(user=request.user)

    animal_filter = AnimalFilter(request.GET, queryset=queryset, request=request) # Pass request to filter
    paginator = Paginator(animal_filter.qs, 10) # 10 animais por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': animal_filter,
        'page_obj': page_obj,
    }
    return render(request, 'herd/animal_list.html', context)

@login_required
@user_passes_test(is_admin, login_url='/')
def animal_create(request):
    """Cria um novo animal."""
    if request.method == 'POST':
        form = AnimalForm(request.POST, user=request.user) # Pass user to form
        if form.is_valid():
            animal = form.save(commit=False)
            animal.user = form.cleaned_data['producer'] # Admin seleciona o produtor
            animal.save()
            messages.success(request, 'Animal cadastrado com sucesso!')
            return redirect('herd:animal_list')
        else:
            messages.error(request, 'Erro ao cadastrar animal. Verifique os dados.')
    else:
        form = AnimalForm(user=request.user) # Pass user to form
    return render(request, 'herd/animal_form.html', {'form': form})

@login_required
@user_passes_test(is_admin, login_url='/')
def animal_update(request, pk):
    """Atualiza um animal existente."""
    animal = get_object_or_404(Animal, pk=pk)
    # Garante que o admin só possa editar animais de produtores
    if not animal.user.profile.user_type == 'producer':
        messages.error(request, 'Você não tem permissão para editar este animal.')
        return redirect('herd:animal_list')

    if request.method == 'POST':
        form = AnimalForm(request.POST, instance=animal, user=request.user) # Pass user to form
        if form.is_valid():
            animal = form.save(commit=False)
            animal.user = form.cleaned_data['producer'] # Admin pode mudar o produtor
            animal.save()
            messages.success(request, 'Animal atualizado com sucesso!')
            return redirect('herd:animal_list')
        else:
            messages.error(request, 'Erro ao atualizar animal. Verifique os dados.')
    else:
        form = AnimalForm(instance=animal, user=request.user) # Pass user to form
    return render(request, 'herd/animal_form.html', {'form': form, 'animal': animal})

@login_required
def animal_detail(request, pk):
    """Exibe os detalhes de um animal específico."""
    animal = get_object_or_404(Animal, pk=pk)
    # Garante que o produtor só possa ver seus próprios animais, a menos que seja admin
    if not request.user.is_staff and animal.user != request.user:
        messages.error(request, 'Você não tem permissão para visualizar este animal.')
        return redirect('herd:animal_list')

    reproductive_events = ReproductiveEvent.objects.filter(animal=animal).order_by('-event_date')
    health_events = HealthEvent.objects.filter(animal=animal).order_by('-event_date')
    return render(request, 'herd/animal_detail.html', {'animal': animal, 'reproductive_events': reproductive_events, 'health_events': health_events})

@login_required
@user_passes_test(is_admin, login_url='/')
def reproductive_event_create(request, animal_pk):
    animal = get_object_or_404(Animal, pk=animal_pk)
    # Garante que o admin só possa adicionar eventos a animais de produtores
    if not animal.user.profile.user_type == 'producer':
        messages.error(request, 'Você não tem permissão para adicionar eventos a este animal.')
        return redirect('herd:animal_detail', pk=animal.pk)

    if request.method == 'POST':
        form = ReproductiveEventForm(request.POST, user=request.user, animal=animal) # Pass user and animal to form
        if form.is_valid():
            event = form.save(commit=False)
            event.animal = animal
            event.user = animal.user # O evento pertence ao produtor do animal
            event.save()
            messages.success(request, 'Evento reprodutivo cadastrado com sucesso!')
            return redirect('herd:animal_detail', pk=animal.pk)
        else:
            messages.error(request, 'Erro ao cadastrar evento reprodutivo. Verifique os dados.')
    else:
        form = ReproductiveEventForm(user=request.user, animal=animal) # Pass user and animal to form
    return render(request, 'herd/reproductive_event_form.html', {'form': form, 'animal': animal})

@login_required
@user_passes_test(is_admin, login_url='/')
def reproductive_event_update(request, pk):
    event = get_object_or_404(ReproductiveEvent, pk=pk)
    # Garante que o admin só possa editar eventos de produtores
    if not event.user.profile.user_type == 'producer':
        messages.error(request, 'Você não tem permissão para editar este evento.')
        return redirect('herd:animal_detail', pk=event.animal.pk)

    if request.method == 'POST':
        form = ReproductiveEventForm(request.POST, instance=event, user=request.user) # Pass user to form
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento reprodutivo atualizado com sucesso!')
            return redirect('herd:animal_detail', pk=event.animal.pk)
        else:
            messages.error(request, 'Erro ao atualizar evento reprodutivo. Verifique os dados.')
    else:
        form = ReproductiveEventForm(instance=event, user=request.user) # Pass user to form
    return render(request, 'herd/reproductive_event_form.html', {'form': form, 'event': event})

@login_required
@user_passes_test(is_admin, login_url='/')
def health_event_create(request, animal_pk):
    animal = get_object_or_404(Animal, pk=animal_pk)
    # Garante que o admin só possa adicionar eventos a animais de produtores
    if not animal.user.profile.user_type == 'producer':
        messages.error(request, 'Você não tem permissão para adicionar eventos a este animal.')
        return redirect('herd:animal_detail', pk=animal.pk)

    if request.method == 'POST':
        form = HealthEventForm(request.POST, user=request.user, animal=animal) # Pass user and animal to form
        if form.is_valid():
            event = form.save(commit=False)
            event.animal = animal
            event.user = animal.user # O evento pertence ao produtor do animal
            event.save()
            messages.success(request, 'Evento sanitário cadastrado com sucesso!')
            return redirect('herd:animal_detail', pk=animal.pk)
        else:
            messages.error(request, 'Erro ao cadastrar evento sanitário. Verifique os dados.')
    else:
        form = HealthEventForm(user=request.user, animal=animal) # Pass user and animal to form
    return render(request, 'herd/health_event_form.html', {'form': form, 'animal': animal})

@login_required
@user_passes_test(is_admin, login_url='/')
def health_event_update(request, pk):
    event = get_object_or_404(HealthEvent, pk=pk)
    # Garante que o admin só possa editar eventos de produtores
    if not event.user.profile.user_type == 'producer':
        messages.error(request, 'Você não tem permissão para editar este evento.')
        return redirect('herd:animal_detail', pk=event.animal.pk)

    if request.method == 'POST':
        form = HealthEventForm(request.POST, instance=event, user=request.user) # Pass user to form
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento sanitário atualizado com sucesso!')
            return redirect('herd:animal_detail', pk=event.animal.pk)
        else:
            messages.error(request, 'Erro ao atualizar evento sanitário. Verifique os dados.')
    else:
        form = HealthEventForm(instance=event, user=request.user) # Pass user to form
    return render(request, 'herd/health_event_form.html', {'form': form, 'event': event})