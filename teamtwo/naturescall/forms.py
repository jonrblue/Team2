from django import forms
class LocationForm(forms.Form):
    location= forms.CharField( widget= forms.TextInput, label='Search Location')
