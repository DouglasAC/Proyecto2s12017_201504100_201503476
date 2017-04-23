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
    #--------RUTA DE CONFIRMACIÓN EN JAVA Y PETICION DE CADENAS DOT------------------
    url(r'^Conectar/', dv_v.Conectar),
    url(r'^ReporteUsuariosDrive', dv_v.reporte_usuarios),
    #--------RUTAS PARA DIRECCIONAMIENTO DE PAGINAS DRIVE---
    url(r'^$', dv_v.index, name='index'),
    url(r'^Drive/LogIn', dv_v.LogInView, name='Drive-logIn'),
    url(r'^Drive/Registro', dv_v.Registro, name='Drive-registro'),
    url(r'^admin/', admin.site.urls),
    #------RUTAS PARA METODOS DE ESTRUCTURAS DRIVE----------
    url(r'^Drive/Registrar', dv_v.registro_usuarios_web, name='drive-reg'),
    url(r'^Drive/Ingresar', dv_v.log_in_usuarios_web, name='drive-ing'),
    #/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/--/-/-/-/-/-/-/-/
    #------RUTAS PARA DIRECCIONAMIENTO EN CALENDAR
    url(r'^Calendar/LogIn', cv_v.log_In_view, name='Calendar-logIn'),
    url(r'^Calendar/Registro', cv_v.reg_view, name='Calendar-registro' ),
    #------RUTAS PARA METODOS DE ESTRUCTURAS EN CALENDAR
    url(r'^Calendar/Registrar', cv_v.registro_usuarios, name='calendar-reg'),
]
