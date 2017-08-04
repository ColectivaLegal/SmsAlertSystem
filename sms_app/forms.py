from django import forms


class AlertForm(forms.Form):
    address = forms.CharField(label='Event Address', max_length=200, widget=forms.Textarea)
