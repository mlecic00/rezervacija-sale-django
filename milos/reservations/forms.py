from django import forms
from .models import Post


class ResUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['sala', 'datum', 'dolazak', 'odlazak', 'razlog', 'napomena']
        widgets = {
            'sala' : forms.Select(attrs={'class':'form-control'}),
            'dolazak' : forms.TimeInput(attrs={'class':'form-control', 'type': 'time'}),
            'odlazak' : forms.TimeInput(attrs={'class':'form-control', 'type': 'time'}),
            'datum' : forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'razlog' : forms.TextInput(attrs={'class':'form-control'}),
            'napomena' : forms.Textarea(attrs={'class':'form-control','placeholder':'Napomena...'})
        }
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['sala', 'ime', 'datum', 'dolazak', 'odlazak', 'razlog', 'napomena']
        widgets = {
            'sala' : forms.Select(attrs={'class':'form-control'}),
            'dolazak' : forms.TimeInput(attrs={'class':'form-control', 'type': 'time'}),
            'odlazak' : forms.TimeInput(attrs={'class':'form-control', 'type': 'time'}),
            'datum' : forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'ime' : forms.Select(attrs={'class':'form-control', 'type': 'text'}),
            'razlog' : forms.TextInput(attrs={'class':'form-control'}),
            'napomena' : forms.Textarea(attrs={'class':'form-control','placeholder':'Napomena...'})
        }
