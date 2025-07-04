import django_filters
from django.contrib.auth.models import User
from users.models import Profile
from .models import Animal
from django import forms

class AnimalFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Nome')
    earring = django_filters.CharFilter(lookup_expr='icontains', label='Brinco')
    status = django_filters.ChoiceFilter(choices=Animal.STATUS_CHOICES, label='Status')
    producer = django_filters.ModelChoiceFilter(
        queryset=User.objects.none(), # Será preenchido no __init__
        field_name='user',
        to_field_name='pk',
        label='Produtor',
        empty_label="Todos os Produtores"
    )

    class Meta:
        model = Animal
        fields = ['name', 'earring', 'status', 'producer']

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
