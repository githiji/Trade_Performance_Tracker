from django import forms


class TradeForm(forms.Form):
    file = forms.FileField(required=True)
    notes = forms.CharField(max_length=250)