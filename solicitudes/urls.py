from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('medios/', views.lista_medios, name='lista_medios'),
    path('solicitar/', views.solicitar_medio, name='solicitar_medio'),
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/solicitudes/', views.aceptar_solicitudes, name='aceptar_solicitudes'),
    path('reportes/', views.reportes_admin, name='reportes_admin'),

]
