from django import forms
from .models import Transaction, Category
from django.contrib.auth.models import User
from users.models import Profile

class TransactionForm(forms.ModelForm):
    producer = forms.ModelChoiceField(
        queryset=User.objects.none(), # Will be set in __init__
        required=False,
        label="Produtor",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'date', 'category', 'description'] # Removed 'user'
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_staff:
            self.fields['producer'].queryset = User.objects.filter(profile__user_type='producer', is_active=True)
            if self.instance and self.instance.pk: # If updating a record
                self.fields['producer'].initial = self.instance.user
            self.fields['producer'].required = True
        else:
            del self.fields['producer']

        self.fields['category'].queryset = Category.objects.all().order_by('name')
        self.fields['category'].required = False # Categoria pode ser opcional

        # Apply form-control class to all fields
        for field_name, field in self.fields.items():
            if field_name != 'producer': # Producer field is already handled
                if isinstance(field.widget, (forms.TextInput, forms.DateInput, forms.NumberInput, forms.Textarea, forms.EmailInput, forms.PasswordInput)):
                    field.widget.attrs.update({'class': 'form-control'})
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select'})
