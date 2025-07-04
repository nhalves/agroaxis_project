from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Transaction
from .forms import TransactionForm
from .filters import TransactionFilter
from milk_quality.models import MilkQuality
from users.models import Profile

@login_required
def transaction_list(request):
    """Exibe a lista de transações financeiras com filtros e paginação."""
    queryset = Transaction.objects.all().order_by('-date')

    if not request.user.is_staff:
        queryset = queryset.filter(user=request.user)

    transaction_filter = TransactionFilter(request.GET, queryset=queryset, request=request) # Pass request to filter
    paginator = Paginator(transaction_filter.qs, 10) # 10 transações por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'filter': transaction_filter,
        'page_obj': page_obj,
    }
    return render(request, 'finance/transaction_list.html', context)

@login_required
def transaction_create(request):
    """Cria uma nova transação financeira."""
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user) # Pass user to form
        if form.is_valid():
            transaction = form.save(commit=False)
            if request.user.is_staff: # Admin seleciona o produtor
                transaction.user = form.cleaned_data['producer']
            else: # Produtor é o próprio usuário logado
                transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transação cadastrada com sucesso!')
            return redirect('finance:transaction_list')
        else:
            messages.error(request, 'Erro ao cadastrar transação. Verifique os dados.')
    else:
        form = TransactionForm(user=request.user) # Pass user to form
    return render(request, 'finance/transaction_form.html', {'form': form})

@login_required
def transaction_update(request, pk):
    """Atualiza uma transação financeira existente."""
    transaction = get_object_or_404(Transaction, pk=pk)
    # Garante que o produtor só possa editar suas próprias transações, a menos que seja admin
    if not request.user.is_staff and transaction.user != request.user:
        messages.error(request, 'Você não tem permissão para editar esta transação.')
        return redirect('finance:transaction_list')

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user) # Pass user to form
        if form.is_valid():
            transaction = form.save(commit=False)
            if request.user.is_staff: # Admin pode mudar o produtor
                transaction.user = form.cleaned_data['producer']
            transaction.save()
            messages.success(request, 'Transação atualizada com sucesso!')
            return redirect('finance:transaction_list')
        else:
            messages.error(request, 'Erro ao atualizar transação. Verifique os dados.')
    else:
        form = TransactionForm(instance=transaction, user=request.user) # Pass user to form
    return render(request, 'finance/transaction_form.html', {'form': form, 'transaction': transaction})

@login_required
def finance_report(request):
    """Exibe o relatório financeiro (custo de produção e fluxo de caixa)."""
    # Lógica para filtrar por produtor se for admin
    queryset = Transaction.objects.all()
    if not request.user.is_staff:
        queryset = queryset.filter(user=request.user)

    total_revenue = queryset.filter(transaction_type='receita').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = queryset.filter(transaction_type='despesa').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_revenue - total_expense

    # Para o cálculo do custo por litro, precisamos do volume de leite do produtor
    # Isso exigiria um filtro de MilkQuality por produtor também.
    # Por enquanto, vamos manter um placeholder ou agregar de forma mais inteligente.
    total_production_volume = MilkQuality.objects.filter(user=request.user).aggregate(Sum('production_volume'))['production_volume__sum'] or 0
    if request.user.is_staff: # Admin pode ver o total de todos os produtores ou de um selecionado
        # Isso precisaria de um filtro de produtor na página de relatório também
        total_production_volume = MilkQuality.objects.all().aggregate(Sum('production_volume'))['production_volume__sum'] or 0

    cost_per_liter = 0
    if total_production_volume > 0:
        cost_per_liter = total_expense / total_production_volume

    context = {
        'total_revenue': total_revenue,
        'total_expense': total_expense,
        'balance': balance,
        'total_production_volume': total_production_volume,
        'cost_per_liter': cost_per_liter,
    }
    return render(request, 'finance/finance_report.html', context)