from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import Profile
from herd.models import Animal, ReproductiveEvent, HealthEvent
from milk_quality.models import MilkQuality
from finance.models import Transaction
from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth
from datetime import date, timedelta, datetime

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
def dashboard(request):
    """Redireciona o usuário para o dashboard correto com base no seu tipo de perfil."""
    if request.user.is_staff:
        return admin_dashboard(request)
    else:
        return producer_dashboard(request)

@login_required
@user_passes_test(lambda u: not u.is_staff, login_url='/')
def producer_dashboard(request):
    """Exibe o dashboard com os dados e indicadores para o produtor rural."""
    template_name = 'core/dashboard.html'
    user = request.user
    today = date.today()

    # --- Milk Quality Data ---
    # Average CCS/CBT for the last month
    last_month_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    recent_milk_quality = MilkQuality.objects.filter(user=user, date__gte=last_month_start, date__lt=today.replace(day=1))
    avg_ccs = recent_milk_quality.aggregate(avg=Avg('ccs'))['avg'] or 0
    avg_cbt = recent_milk_quality.aggregate(avg=Avg('cbt'))['avg'] or 0

    # Milk Production Chart Data (last 6 months)
    six_months_ago = today - timedelta(days=180)
    milk_production_data = MilkQuality.objects.filter(user=user, date__gte=six_months_ago).annotate(month=TruncMonth('date')).values('month').annotate(total_volume=Sum('production_volume')).order_by('month')
    milk_chart_labels = [data['month'].strftime('%b/%Y') for data in milk_production_data]
    milk_chart_volumes = [float(data['total_volume']) for data in milk_production_data]

    # CCS/CBT Evolution Chart Data (last 6 months)
    ccs_cbt_data = MilkQuality.objects.filter(user=user, date__gte=six_months_ago).annotate(month=TruncMonth('date')).values('month').annotate(avg_ccs=Avg('ccs'), avg_cbt=Avg('cbt')).order_by('month')
    ccs_chart_labels = [data['month'].strftime('%b/%Y') for data in ccs_cbt_data]
    ccs_chart_values = [float(data['avg_ccs']) for data in ccs_cbt_data]
    cbt_chart_values = [float(data['avg_cbt']) for data in ccs_cbt_data]

    # --- Financial Data ---
    # Current Month Revenue/Expense
    current_month_transactions = Transaction.objects.filter(user=user, date__year=today.year, date__month=today.month)
    monthly_revenue = current_month_transactions.filter(transaction_type='receita').aggregate(total=Sum('amount'))['total'] or 0
    monthly_expense = current_month_transactions.filter(transaction_type='despesa').aggregate(total=Sum('amount'))['total'] or 0

    # Cash Flow Chart Data (last 6 months)
    finance_data = Transaction.objects.filter(user=user, date__gte=six_months_ago).annotate(month=TruncMonth('date')).values('month', 'transaction_type').annotate(total_amount=Sum('amount')).order_by('month')
    
    finance_labels_set = set()
    for data in finance_data:
        finance_labels_set.add(data['month'].strftime('%b/%Y'))
    finance_labels = sorted(list(finance_labels_set), key=lambda x: datetime.strptime(x, '%b/%Y')) # Sort by date

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

    # --- Alerts ---
    alerts = []

    # Example: High CCS alert
    if avg_ccs > 400: # Threshold for alert
        alerts.append(f"Alerta: CCS média do último mês ({avg_ccs:.0f}) está alta. Verifique a qualidade do leite.")

    # Example: Overdue reproductive events (e.g., cows not pregnant after 90 days post-partum)
    # This would require more complex logic and data from Animal and ReproductiveEvent models
    # For now, a placeholder.
    # cows_not_pregnant = Animal.objects.filter(user=user, status='lactating', last_calving_date__lte=today - timedelta(days=90), is_pregnant=False).count()
    # if cows_not_pregnant > 0:
    #     alerts.append(f"Alerta: {cows_not_pregnant} vacas com mais de 90 dias pós-parto e não gestantes.")

    context = {
        'avg_ccs': avg_ccs,
        'avg_cbt': avg_cbt,
        'monthly_revenue': monthly_revenue,
        'monthly_expense': monthly_expense,
        'alerts': alerts,
        'milk_chart_labels': milk_chart_labels,
        'milk_chart_volumes': milk_chart_volumes,
        'ccs_chart_labels': ccs_chart_labels,
        'ccs_chart_values': ccs_chart_values,
        'cbt_chart_values': cbt_chart_values,
        'finance_labels': finance_labels,
        'finance_revenues': finance_revenues,
        'finance_expenses': finance_expenses,
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Exibe o dashboard de administração com a lista de produtores e seus status."""
    template_name = 'core/admin_dashboard.html'

    producers = Profile.objects.filter(user_type='producer')

    total_producers = producers.count()
    active_producers = producers.filter(user__is_active=True).count()
    inactive_producers = producers.filter(user__is_active=False).count()

    for p in producers:
        # Initialize health indicator
        p.health_indicator = 'success' # Default to green

        # Check for inactive status
        if not p.user.is_active:
            p.health_indicator = 'secondary' # Grey for inactive
            continue # No need to check further if inactive

        # Check Milk Quality (CCS)
        last_30_days = date.today() - timedelta(days=30)
        recent_milk_quality = MilkQuality.objects.filter(user=p.user, date__gte=last_30_days)
        avg_ccs = recent_milk_quality.aggregate(avg_ccs=Avg('ccs'))['avg_ccs']

        if avg_ccs is None: # No milk quality data
            p.health_indicator = 'warning' # Yellow for no data
        elif avg_ccs > 500: # Example threshold for high CCS
            p.health_indicator = 'danger' # Red for critical CCS
        elif avg_ccs > 300: # Example threshold for elevated CCS
            p.health_indicator = 'warning' # Yellow for elevated CCS

        # Check recent financial activity (e.g., last 60 days)
        last_60_days = date.today() - timedelta(days=60)
        has_recent_finance_activity = Transaction.objects.filter(user=p.user, date__gte=last_60_days).exists()
        if not has_recent_finance_activity and p.health_indicator != 'danger': # Don't override red
            p.health_indicator = 'warning' # Yellow if no recent finance activity

        # Add a custom attribute for display in template
        p.display_status = "Ativo" if p.user.is_active else "Inativo"


    context = {
        'producers': producers,
        'total_producers': total_producers,
        'active_producers': active_producers,
        'inactive_producers': inactive_producers,
    }
    return render(request, template_name, context)