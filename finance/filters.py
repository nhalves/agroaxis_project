import django_filters
from django.contrib.auth.models import User
from users.models import Profile
from .models import Transaction
from django import forms

class TransactionFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(lookup_expr='exact', label='Data (AAAA-MM-DD)')
    transaction_type = django_filters.ChoiceFilter(choices=Transaction.TRANSACTION_TYPE_CHOICES, label='Tipo', field_name='transaction_type')
    category__name = django_filters.CharFilter(lookup_expr='icontains', label='Categoria')
    producer = django_filters.ModelChoiceFilter(
        queryset=User.objects.none(), # Será preenchido no __init__
        field_name='user',
        to_field_name='pk',
        label='Produtor',
        empty_label="Todos os Produtores"
    )

    class Meta:
        model = Transaction
        fields = ['date', 'transaction_type', 'category__name', 'producer']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request and self.request.user.is_staff:
            self.filters['producer'].queryset = User.objects.filter(profile__user_type='producer', is_active=True)
        else:
            del self.filters['producer']

        # Adiciona classes CSS aos widgets
        for field_name, field in self.form.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
