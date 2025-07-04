from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Profile
from finance.models import Transaction
from milk_quality.models import MilkQuality
from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth
from datetime import date, timedelta, datetime

@login_required
def analysis_dashboard(request):
    context = {}
    user = request.user
    
    # Se o usuário for admin, ele pode filtrar por produtor
    selected_producer_id = request.GET.get('producer')
    selected_producer = None

    if user.is_staff:
        producers = Profile.objects.filter(user_type='producer')
        context['producers'] = producers
        if selected_producer_id:
            selected_producer = Profile.objects.get(pk=selected_producer_id).user
        else:
            # Se for admin e nenhum produtor selecionado, mostra dados agregados ou do primeiro produtor
            if producers.exists():
                selected_producer = producers.first().user
    else: # Se for produtor, só vê os próprios dados
        selected_producer = user

    if selected_producer:
        # Lógica para coletar dados para gráficos e relatórios
        today = date.today()
        six_months_ago = today - timedelta(days=180)

        # Dados de Qualidade do Leite
        milk_production_data = MilkQuality.objects.filter(user=selected_producer, production_volume__isnull=False, date__gte=six_months_ago).annotate(month=TruncMonth('date')).values('month').annotate(total_volume=Sum('production_volume')).order_by('month')
        milk_chart_labels = [data['month'].strftime('%b/%Y') for data in milk_production_data]
        milk_chart_volumes = [float(data['total_volume']) for data in milk_production_data]

        ccs_cbt_data = MilkQuality.objects.filter(user=selected_producer, date__gte=six_months_ago).annotate(month=TruncMonth('date')).values('month').annotate(avg_ccs=Avg('ccs'), avg_cbt=Avg('cbt')).order_by('month')
        ccs_chart_labels = [data['month'].strftime('%b/%Y') for data in ccs_cbt_data]
        ccs_chart_values = [float(data['avg_ccs']) for data in ccs_cbt_data]
        cbt_chart_values = [float(data['avg_cbt']) for data in ccs_cbt_data]

        # Dados Financeiros
        finance_data = Transaction.objects.filter(user=selected_producer, date__gte=six_months_ago).annotate(month=TruncMonth('date')).values('month', 'transaction_type').annotate(total_amount=Sum('amount')).order_by('month')
        
        finance_labels_set = set()
        for data in finance_data:
            finance_labels_set.add(data['month'].strftime('%b/%Y'))
        finance_labels = sorted(list(finance_labels_set), key=lambda x: datetime.strptime(x, '%b/%Y'))

        revenues_by_month = {label: 0 for label in finance_labels}
        expenses_by_month = {label: 0 for label in finance_labels}

        for data in finance_data:
            month_str = data['month'].strftime('%b/%Y')
            if data['transaction_type'] == 'receita':
                revenues_by_month[month_str] += float(data['total_amount'])
            else:
                expenses_by_month[month_str] += float(data['total_amount'])

        finance_revenues = [revenues_by_month[label] for label in finance_labels]
        finance_expenses = [expenses_by_month[label] for label in finance_labels]

        context.update({
            'selected_producer': selected_producer,
            'milk_chart_labels': milk_chart_labels,
            'milk_chart_volumes': milk_chart_volumes,
            'ccs_chart_labels': ccs_chart_labels,
            'ccs_chart_values': ccs_chart_values,
            'cbt_chart_values': cbt_chart_values,
            'finance_labels': finance_labels,
            'finance_revenues': finance_revenues,
            'finance_expenses': finance_expenses,
        })

    return render(request, 'analysis/analysis_dashboard.html', context)