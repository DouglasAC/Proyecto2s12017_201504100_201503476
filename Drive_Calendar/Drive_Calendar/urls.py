"""Drive_Calendar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Drive_Calendar import views as dv_v # IMPORTANDO EL CONTROLADOR DE VISTAS PARA DRIVE
from Drive_Calendar import views_C as cv_v # IMPORTANDO EL CONTROLADOR DE VISTAS PARA CALENDAR

urlpatterns = [
    #--------RUTA DE CONFIRMACIÓN EN JAVA Y PETICION DE CADENAS DOT DE DRIVE------------------
    url(r'^Conectar/', dv_v.Conectar),
    url(r'^ReporteUsuariosDrive', dv_v.reporte_usuarios),
    url(r'^Historial_Drive', dv_v.reporte_bitacora),
    #--------PETICION DE CADENAS DOT DE CALENDAR---------------------------------
    url(r'^ReporteUsuariosCalendar', cv_v.reporte_usuarios),
    url(r'^Historial_Calendar', cv_v.reporte_bitacora),
    #--------RUTAS PARA DIRECCIONAMIENTO DE PAGINAS DRIVE---
    url(r'^$', dv_v.index, name='index'),
    url(r'^Drive/LogIn', dv_v.LogInView, name='Drive-logIn'),
    url(r'^Drive/Registro', dv_v.Registro, name='Drive-registro'),
    url(r'^admin/', admin.site.urls),
    #------RUTAS PARA METODOS DE ESTRUCTURAS DRIVE----------
    url(r'^Drive/Registrar', dv_v.registro_usuarios_web, name='drive-reg'),
    url(r'^Drive/Ingresar', dv_v.log_in_usuarios_web, name='drive-ing'),
    url(r'^Drive/Bitacora', dv_v.guardar_cambios, name='bitacora-drive'),#ESTA PUEDO ELIMINARLA
    #------RUTAS PARA METODOS DE ESTRUCTURA DRIVE DESDE ANDROID---------
    url(r'^Drive/Android/Registrar', dv_v.registro_usuarios_android),
    url(r'^Drive/Android/LogIn', dv_v.log_in_usuarios_Android),
    #/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/--/-/-/-/-/-/-/-/
    #------RUTAS PARA DIRECCIONAMIENTO EN CALENDAR
    url(r'^Calendar/LogIn', cv_v.log_In_view, name='Calendar-logIn'),
    url(r'^Calendar/Registro', cv_v.reg_view, name='Calendar-registro' ),
    #------RUTAS PARA METODOS DE ESTRUCTURAS EN CALENDAR
    url(r'^Calendar/Registrar', cv_v.registro_usuarios, name='calendar-reg'),
    url(r'^Calendar/Ingresar', cv_v.log_in_usuarios, name='calendar-ing'),
    #------RUTAS PARA METODOS DE ESTRUCTURAS EN CALENDAR DESDE ANDROID
    url(r'^Calendar/Android/Registrar', cv_v.registro_usuarios_android),
    url(r'^Calendar/Android/LogIn', cv_v.log_in_usuarios_Android),
    #PRUEBAS
    url(r'^file', dv_v.file_upload, name='filep'),
    url(r'^form_file', dv_v.file_view),
]
