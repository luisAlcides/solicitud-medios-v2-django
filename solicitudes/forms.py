from django import forms
from .models import Solicitud, Aula, Medio, Perfil
from django.utils import timezone
from datetime import timedelta
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['medio', 'aula', 'fecha', 'hora', 'comentario']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'comentario': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        today = timezone.now().date()
        max_date = today + timedelta(days=10)
        self.fields['fecha'].widget.attrs.update({
            'min': today.strftime('%Y-%m-%d'),
            'max': max_date.strftime('%Y-%m-%d'),
        })

        self.fields['hora'].widget.attrs.update({
            'min': '07:00',
            'max': '17:00',
        })

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            today = timezone.now().date()
            max_date = today + timedelta(days=10)
            if fecha < today:
                raise forms.ValidationError("La fecha seleccionada ya ha pasado. Por favor, elige una fecha válida.")
            if fecha > max_date:
                raise forms.ValidationError("No puedes solicitar un medio con más de 10 días de anticipación.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        medio = cleaned_data.get('medio')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if medio and fecha and hora:
            if Solicitud.objects.filter(medio=medio, fecha=fecha, hora=hora).exists():
                raise forms.ValidationError("Este equipo ya ha sido solicitado para la fecha y hora seleccionadas.")

        return cleaned_data

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['departamento']