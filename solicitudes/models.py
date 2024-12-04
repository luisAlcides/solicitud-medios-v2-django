from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Medio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Aula(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('RECHAZADA', 'Rechazada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    medio = models.ForeignKey(Medio, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    comentario = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.usuario.username} - {self.medio.nombre} - {self.aula.nombre} - {self.fecha} {self.hora}"


class Perfil(models.Model):
    USER_ROLES = [
        ('PROFESOR', 'Profesor'),
        ('ADMIN', 'Administrador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=USER_ROLES, default='PROFESOR')
    departamento = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    instance.perfil.save()