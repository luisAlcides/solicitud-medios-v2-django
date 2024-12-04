from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import weasyprint

from .models import Medio, Solicitud, Aula
from .forms import SolicitudForm, PerfilForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
import datetime
from django.db.models import Count
from django.utils import timezone
from django.template.loader import get_template
from solicitudes import models


def home(request):
    return render(request, 'solicitudes/home.html')

@login_required
def lista_medios(request):
    medios = Medio.objects.all()
    return render(request, 'solicitudes/lista_medios.html', {'medios': medios})

@login_required
def solicitar_medio(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.save()
            messages.success(request, 'Solicitud creada exitosamente.')
            return redirect('lista_solicitudes')
        else:
            messages.error(request, 'Hubo un error al crear la solicitud. Por favor, verifica los datos ingresados. posiblemente estas procesando un mismo medio que otro profesor')
    else:
        form = SolicitudForm()

    return render(request, 'solicitudes/solicitar_medio.html', {'form': form})
@login_required
def lista_solicitudes(request):
    if request.user.is_staff:
        solicitudes = Solicitud.objects.all().order_by('-fecha', '-hora')
    else:
        solicitudes = Solicitud.objects.filter(usuario=request.user).order_by('-fecha', '-hora')
    return render(request, 'solicitudes/lista_solicitudes.html', {'solicitudes': solicitudes})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Usuario o contraseña incorrectos."
            return render(request, 'solicitudes/login.html', {'error': error})
    return render(request, 'solicitudes/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def perfil_usuario(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil_usuario')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'solicitudes/perfil_usuario.html', {'form': form})

@staff_member_required
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    if request.method == 'POST':
        solicitud.estado = 'CONFIRMADA'
        solicitud.save()
        messages.success(request, f"Solicitud {solicitud.id} aprobada correctamente.")
        return redirect('lista_solicitudes_admin')
    return render(request, 'solicitudes/confirmar_aprobacion.html', {'solicitud': solicitud})


def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def aceptar_solicitudes(request):
    solicitudes_pendientes = Solicitud.objects.filter(estado='pendiente').order_by('-creado_en')

    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        accion = request.POST.get('accion')

        solicitud = get_object_or_404(Solicitud, id=solicitud_id)

        if accion == 'aceptar':
            solicitud.estado = 'aceptada'
            solicitud.save()
            messages.success(request, f"Solicitud de {solicitud.usuario.username} aceptada correctamente.")
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
            solicitud.save()
            messages.warning(request, f"Solicitud de {solicitud.usuario.username} rechazada.")
        else:
            messages.error(request, "Acción inválida.")

        return redirect('aceptar_solicitudes')

    context = {
        'solicitudes': solicitudes_pendientes
    }
    return render(request, 'solicitudes/aceptar_solicitudes.html', context)


@user_passes_test(is_admin)
def reportes_admin(request):
    solicitudes = Solicitud.objects.all().order_by('-creado_en')

    context = {
        'solicitudes': solicitudes,
        'usuario': request.user,
    }

    template = get_template('solicitudes/reportes_admin.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lista_solicitudes.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

    return response