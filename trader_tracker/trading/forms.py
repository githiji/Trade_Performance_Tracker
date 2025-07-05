from django import forms
from .models import Tag, Trade,UserProfile, JournalEntry
   

class TradeForm(forms.ModelForm):
    file = forms.FileField(required=False)
    class Meta:
        model = Trade
        fields = ['file', 'notes', 'tags', 'followed_strategy', 'strategy_outcome']  # Add 'tags' here
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),  # Or use SelectMultiple for dropdown
        }


class StartingBalanceForm(forms.ModelForm):
    starting_balance = forms.IntegerField(required=False)
    class Meta:
        model = UserProfile
        fields = ['starting_balance']
        widgets = {
            'starting_balance': forms.NumberInput(attrs={
                'class': 'border rounded px-2 py-1 w-full',
                'placeholder': 'Starting balance',
            })
        }

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['trade', 'entry', 'emotion', 'session', 'chart_image']
        widgets = {
            'entry': forms.Textarea(attrs={'rows': 4}),
            'emotion': forms.TextInput(attrs={'placeholder': 'e.g., confident, anxious'}),
        }   

