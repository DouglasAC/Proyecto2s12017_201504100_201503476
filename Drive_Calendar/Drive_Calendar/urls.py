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
    url(r'^conectar', dv_v.conAndroid),
    url(r'^ReporteUsuariosDrive', dv_v.reporte_usuarios),
    url(r'^Historial_Drive', dv_v.reporte_bitacora),
    url(r'^Drive_Directorio', dv_v.reporte_directorio),
    url(r'^Drive_Archivos', dv_v.reporte_avl),
    #--------PETICION DE CADENAS DOT DE CALENDAR---------------------------------
    url(r'^ReporteUsuariosCalendar', cv_v.reporte_usuarios),
    url(r'^Historial_Calendar', cv_v.reporte_bitacora),
    url(r'^Reporte_matriz', cv_v.reporte_matriz),
    url(r'^tablahash', cv_v.reporte_hash),
    #--------RUTAS PARA DIRECCIONAMIENTO DE PAGINAS DRIVE---
    url(r'^$', dv_v.index, name='index'),
    url(r'^Drive/LogIn', dv_v.LogInView, name='Drive-logIn'),
    url(r'^Drive/Registro', dv_v.Registro, name='Drive-registro'),
    url(r'^admin/', admin.site.urls),
    url(r'^Drive/Carpetas', dv_v.listar_folder_path, name='Drive-carp'),
    url(r'^Drive/Nueva_Carpeta', dv_v.add_folder, name="add_carpetas"),
    url(r'^Drive/Upload', dv_v.vista_upload, name="vista_upload"),
    #------RUTAS PARA METODOS DE ESTRUCTURAS DRIVE----------
    url(r'^Drive/Registrar', dv_v.registro_usuarios_web, name='drive-reg'),
    url(r'^Drive/Ingresar', dv_v.log_in_usuarios_web, name='drive-ing'),
    url(r'^Drive/Editar/(?P<path>[\w\-]+)/$', dv_v.editar_folder_path, name='edit-folder'),
    url(r'^Drive/Nueva/Carpeta', dv_v.new_folder, name="add_folder"),
    url(r'^Drive/Nuevo/Archivo', dv_v.new_file, name="add-file"),
    url(r'^Drive/Bitacora', dv_v.guardar_cambios, name='bitacora-drive'),#ESTA PUEDO ELIMINARLA
    #------RUTAS PARA METODOS DE ESTRUCTURA DRIVE DESDE ANDROID---------
    url(r'^Drive/Android/Registrar', dv_v.registro_usuarios_android),
    url(r'^Drive/Android/LogIn', dv_v.log_in_usuarios_Android),
    #/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/--/-/-/-/-/-/-/-/
    #------RUTAS PARA DIRECCIONAMIENTO EN CALENDAR
    url(r'^Calendar/LogIn', cv_v.log_In_view, name='Calendar-logIn'),
    url(r'^Calendar/Registro', cv_v.reg_view, name='Calendar-registro' ),
    url(r'^Calendar/Nuevo/Evento', cv_v.view_crear_eventos, name='cal-v-e'),
    url(r'^Calendar/Android/NuevoE', cv_v.eventos_android),
    #------RUTAS PARA METODOS DE ESTRUCTURAS EN CALENDAR
    url(r'^Calendar/Registrar', cv_v.registro_usuarios, name='calendar-reg'),
    url(r'^Calendar/Ingresar', cv_v.log_in_usuarios, name='calendar-ing'),
    url(r'^Calendar/Creando/Evento', cv_v.ingresar_Evento, name='ing-mat'),
    #------RUTAS PARA METODOS DE ESTRUCTURAS EN CALENDAR DESDE ANDROID
    url(r'^Calendar/Android/Registrar', cv_v.registro_usuarios_android),
    url(r'^Calendar/Android/LogIn', cv_v.log_in_usuarios_Android),
    #PRUEBAS
    url(r'^file', dv_v.file_upload, name='filep'),
    url(r'^form_file', dv_v.file_view),
    url(r'^Calendar/Android/serializar', cv_v.prueba),
]
