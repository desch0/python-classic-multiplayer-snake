from django import forms

class NameForm(forms.Form):
	name = forms.CharField(label='', max_length=40, widget=forms.TextInput(attrs={'class':'input_name', 'placeholder': 'Username'}))
