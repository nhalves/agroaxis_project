from django import forms
from .models import Animal, ReproductiveEvent, HealthEvent
from django.contrib.auth.models import User
from users.models import Profile

class AnimalForm(forms.ModelForm):
    producer = forms.ModelChoiceField(
        queryset=User.objects.none(), # Will be set in __init__
        required=False,
        label="Produtor",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Animal
        fields = ['earring', 'name', 'birth_date', 'breed', 'status'] # Removed 'user'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'earring': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_staff:
            self.fields['producer'].queryset = User.objects.filter(profile__user_type='producer', is_active=True)
            if self.instance and self.instance.pk: # If updating an animal
                self.fields['producer'].initial = self.instance.user
            self.fields['producer'].required = True
        else:
            del self.fields['producer']

        # Apply form-control class to all fields
        for field_name, field in self.fields.items():
            if field_name != 'producer': # Producer field is already handled
                if isinstance(field.widget, (forms.TextInput, forms.DateInput, forms.NumberInput, forms.Textarea, forms.EmailInput, forms.PasswordInput)):
                    field.widget.attrs.update({'class': 'form-control'})
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select'})


class ReproductiveEventForm(forms.ModelForm):
    class Meta:
        model = ReproductiveEvent
        fields = ['animal', 'event_type', 'event_date', 'description'] # Removed 'user'
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'animal': forms.Select(attrs={'class': 'form-select'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        animal = kwargs.pop('animal', None) # Animal instance passed from view
        super().__init__(*args, **kwargs)

        if user and not user.is_staff: # If not admin, filter animals by user
            self.fields['animal'].queryset = Animal.objects.filter(user=user)
        
        # If animal is passed, set it as initial and disable the field
        if animal:
            self.fields['animal'].initial = animal
            self.fields['animal'].widget.attrs['disabled'] = 'disabled'

        # Apply form-control class to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.DateInput, forms.NumberInput, forms.Textarea, forms.EmailInput, forms.PasswordInput)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})


class HealthEventForm(forms.ModelForm):
    class Meta:
        model = HealthEvent
        fields = ['animal', 'event_type', 'event_date', 'description', 'medication', 'withdrawal_period_days'] # Removed 'user'
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'animal': forms.Select(attrs={'class': 'form-select'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medication': forms.TextInput(attrs={'class': 'form-control'}),
            'withdrawal_period_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        animal = kwargs.pop('animal', None) # Animal instance passed from view
        super().__init__(*args, **kwargs)

        if user and not user.is_staff: # If not admin, filter animals by user
            self.fields['animal'].queryset = Animal.objects.filter(user=user)

        # If animal is passed, set it as initial and disable the field
        if animal:
            self.fields['animal'].initial = animal
            self.fields['animal'].widget.attrs['disabled'] = 'disabled'

        # Apply form-control class to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.DateInput, forms.NumberInput, forms.Textarea, forms.EmailInput, forms.PasswordInput)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
