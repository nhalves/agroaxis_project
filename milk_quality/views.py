from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import MilkQuality
from .forms import MilkQualityForm
from .filters import MilkQualityFilter
from users.models import Profile
from herd.models import Animal

@login_required
def milk_quality_list(request):
    """Exibe a lista de registros de qualidade do leite com filtros e paginação."""
    queryset = MilkQuality.objects.all().order_by('-date', 'animal__name')

    if not request.user.is_staff:
        queryset = queryset.filter(user=request.user)

    milk_records_filter = MilkQualityFilter(request.GET, queryset=queryset, request=request) # Pass request to filter
    paginator = Paginator(milk_records_filter.qs, 10) # 10 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'filter': milk_records_filter,
        'page_obj': page_obj,
    }
    return render(request, 'milk_quality/milk_quality_list.html', context)

@login_required
def milk_quality_create(request):
    """Cria um novo registro de qualidade do leite."""
    if request.method == 'POST':
        form = MilkQualityForm(request.POST, user=request.user) # Pass user to form
        if form.is_valid():
            record = form.save(commit=False)
            if request.user.is_staff: # Admin seleciona o produtor
                record.user = form.cleaned_data['producer']
            else: # Produtor é o próprio usuário logado
                record.user = request.user
            record.save()
            messages.success(request, 'Registro de qualidade do leite cadastrado com sucesso!')
            return redirect('milk_quality:milk_quality_list')
        else:
            messages.error(request, 'Erro ao cadastrar registro de qualidade do leite. Verifique os dados.')
    else:
        form = MilkQualityForm(user=request.user) # Pass user to form
    return render(request, 'milk_quality/milk_quality_form.html', {'form': form})

@login_required
def milk_quality_update(request, pk):
    """Atualiza um registro de qualidade do leite existente."""
    record = get_object_or_404(MilkQuality, pk=pk)
    # Garante que o produtor só possa editar seus próprios registros, a menos que seja admin
    if not request.user.is_staff and record.user != request.user:
        messages.error(request, 'Você não tem permissão para editar este registro.')
        return redirect('milk_quality:milk_quality_list')

    if request.method == 'POST':
        form = MilkQualityForm(request.POST, instance=record, user=request.user) # Pass user to form
        if form.is_valid():
            record = form.save(commit=False)
            if request.user.is_staff: # Admin pode mudar o produtor
                record.user = form.cleaned_data['producer']
            record.save()
            messages.success(request, 'Registro de qualidade do leite atualizado com sucesso!')
            return redirect('milk_quality:milk_quality_list')
        else:
            messages.error(request, 'Erro ao atualizar registro de qualidade do leite. Verifique os dados.')
    else:
        form = MilkQualityForm(instance=record, user=request.user) # Pass user to form
    return render(request, 'milk_quality/milk_quality_form.html', {'form': form, 'record': record})