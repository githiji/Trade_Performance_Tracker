from django import forms
from .models import Tag, Trade,UserProfile

class TradeForm(forms.ModelForm):
    file = forms.FileField(required=False)
    class Meta:
        model = Trade
        fields = ['file', 'notes', 'tags']  # Add 'tags' here
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),  # Or use SelectMultiple for dropdown
        }


class StartingBalanceForm(forms.ModelForm):
    starting_balance = forms.BooleanField(required=False)
    class Meta:
        model = UserProfile
        fields = ['starting_balance']
        widgets = {
            'starting_balance': forms.NumberInput(attrs={
                'class': 'border rounded px-2 py-1 w-full',
                'placeholder': 'Starting balance',
            })
        }