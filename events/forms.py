from django import forms
from django.core.exceptions import ValidationError
from .models import Event, Participant, Category


class CategoryForm(forms.ModelForm):
    """Form for creating and updating categories"""

    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'input-field',
                'rows': 3,
                'placeholder': 'Enter category description'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Check for duplicate (excluding current instance if editing)
            exists = Category.objects.filter(name__iexact=name)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise ValidationError('A category with this name already exists.')
        return name.strip()


class EventForm(forms.ModelForm):
    """Form for creating and updating events"""

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter event name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'input-field',
                'rows': 4,
                'placeholder': 'Enter event description'
            }),
            'date': forms.DateInput(attrs={
                'class': 'input-field',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'input-field',
                'type': 'time'
            }),
            'location': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter event location'
            }),
            'category': forms.Select(attrs={
                'class': 'input-field'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.strip()
        return name

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date:
            from django.utils import timezone
            from datetime import date as date_class
            if date < date_class.today():
                # Allow past dates for editing existing events
                if not self.instance.pk:
                    raise ValidationError('Event date cannot be in the past.')
        return date


class ParticipantForm(forms.ModelForm):
    """Form for creating and updating participants"""

    class Meta:
        model = Participant
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter participant name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter participant email'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.strip()
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check for duplicate (excluding current instance if editing)
            exists = Participant.objects.filter(email__iexact=email)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise ValidationError('A participant with this email already exists.')
        return email


class ParticipantSelectionForm(forms.ModelForm):
    """Form for selecting participants for an event"""
    participants = forms.ModelMultipleChoiceField(
        queryset=Participant.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-checkbox h-5 w-5 text-indigo-600'
        }),
        required=False
    )

    class Meta:
        model = Event
        fields = ['participants']


class EventFilterForm(forms.Form):
    """Form for filtering events"""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={
            'class': 'input-field'
        })
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'input-field',
            'type': 'date'
        })
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'input-field',
            'type': 'date'
        })
    )


class SearchForm(forms.Form):
    """Form for search functionality"""
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
            'placeholder': 'Search events by name or location...'
        })
    )
