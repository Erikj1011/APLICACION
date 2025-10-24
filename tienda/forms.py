from django import forms
from .models import Resena

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['comentario', 'calificacion']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows':4, 'placeholder':'Escribe tu reseña...'}),
            'calificacion': forms.NumberInput(attrs={'min':1, 'max':5}),
        }
