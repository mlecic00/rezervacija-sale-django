from django import forms
from .models import Post
from django.core.exceptions import ValidationError
#from django.core.validators import MaxLengthValidator
from django.db.models import Q


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
    
    def clean(self):
        cleaned_data = super().clean()
        sala = cleaned_data.get('sala')
        dolazak = cleaned_data.get('dolazak')
        odlazak = cleaned_data.get('odlazak')
        datum = cleaned_data.get('datum')

        if sala and dolazak and odlazak and datum:
            conflicting_reservations = Post.objects.filter(
                Q(dolazak__lt=odlazak, odlazak__gt=dolazak) |  
                Q(dolazak__lte=dolazak, odlazak__gte=odlazak),
                sala=sala,
                datum=datum 
            ).exclude(id=self.instance.id)  # Exclude current instance if updating
            if conflicting_reservations.exists():
                raise ValidationError("Sala je bukirana u ovo vreme!")

        return cleaned_data
    
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

    def clean(self):
        cleaned_data = super().clean()
        sala = cleaned_data.get('sala')
        dolazak = cleaned_data.get('dolazak')
        odlazak = cleaned_data.get('odlazak')
        datum = cleaned_data.get('datum')

        if sala and dolazak and odlazak and datum:
            conflicting_reservations = Post.objects.filter(
                Q(dolazak__lt=odlazak, odlazak__gt=dolazak) |  
                Q(dolazak__lte=dolazak, odlazak__gte=odlazak),
                sala=sala,
                datum=datum 
            ).exclude(id=self.instance.id)  # Exclude current instance if updating
            if conflicting_reservations.exists():
                raise ValidationError("Sala je bukirana u ovo vreme!")

        return cleaned_data