from django import forms
from .models import MilkQuality
from herd.models import Animal
from django.contrib.auth.models import User
from users.models import Profile

class MilkQualityForm(forms.ModelForm):
    producer = forms.ModelChoiceField(
        queryset=User.objects.none(), # Will be set in __init__
        required=False,
        label="Produtor",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = MilkQuality
        fields = ['animal', 'date', 'ccs', 'cbt', 'production_volume'] # Removed 'user'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'animal': forms.Select(attrs={'class': 'form-select'}),
            'ccs': forms.NumberInput(attrs={'class': 'form-control'}),
            'cbt': forms.NumberInput(attrs={'class': 'form-control'}),
            'production_volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_staff:
            self.fields['producer'].queryset = User.objects.filter(profile__user_type='producer', is_active=True)
            if self.instance and self.instance.pk: # If updating a record
                self.fields['producer'].initial = self.instance.user
            self.fields['producer'].required = True
            # Filter animals by selected producer if any, otherwise all animals
            if self.data.get('producer'):
                selected_producer_id = self.data.get('producer')
                self.fields['animal'].queryset = Animal.objects.filter(user__pk=selected_producer_id).order_by('name')
            elif self.instance and self.instance.pk: # If editing, show animals of current record's user
                self.fields['animal'].queryset = Animal.objects.filter(user=self.instance.user).order_by('name')
            else:
                self.fields['animal'].queryset = Animal.objects.none() # No producer selected, no animals
        else:
            del self.fields['producer']
            self.fields['animal'].queryset = Animal.objects.filter(user=user).order_by('name')

        # Apply form-control class to all fields
        for field_name, field in self.fields.items():
            if field_name != 'producer': # Producer field is already handled
                if isinstance(field.widget, (forms.TextInput, forms.DateInput, forms.NumberInput, forms.Textarea, forms.EmailInput, forms.PasswordInput)):
                    field.widget.attrs.update({'class': 'form-control'})
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select'})
