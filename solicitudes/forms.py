from django import forms
from .models import Solicitud, Aula, Medio, Perfil

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['medio', 'aula', 'fecha', 'hora', 'comentario']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'comentario': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        medio = cleaned_data.get('medio')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if Solicitud.objects.filter(medio=medio, fecha=fecha, hora=hora).exists():
            raise forms.ValidationError("Este equipo ya ha sido solicitado para la fecha y hora seleccionadas.")

        return cleaned_data

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['departamento']