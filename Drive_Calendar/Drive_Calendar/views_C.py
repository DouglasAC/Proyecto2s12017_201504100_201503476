from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt #Utilizo este import para hacer que ciertas urls no tengan protección por csrf
from Drive_Calendar.Calendar_EDD import Lista
from Drive_Calendar.Calendar_EDD import Bitacora
from django.http import HttpResponse

# ESTE ES EL MANEJO DE VISTAS DE CALENDAR

# ESTRUCTURAS CALENDAR
lista_usuario = Lista.ListaDoble()
bitacora_cambios_c = Bitacora.Bitacora()

#CONEXION CON JAVA Y REPORTES DE CALENDAR
def reporte_usuarios(request):
    cadena = lista_usuario.cadena_Dot()
    return HttpResponse(cadena)

def reporte_bitacora(request):
    cadena = bitacora_cambios_c.listar_bitadora()
    return HttpResponse("| Historial de Calendar |\n"+cadena)

# FUNCIONES PARA MANEJAR EL REDIRECCIONAMIENTO ENTRE PAGINAS CALENDAR
def log_In_view(request):

    return render(request, 'LogIn_Calendar.html')

def reg_view(request):

    return render(request, 'Registro_Calendar.html')

# FUNCIONES PARA MANEJAR EL INGRESO DE DATOS EN CALENDAR

def registro_usuarios(request):
    if request.method == 'POST':
        nombre = request.POST['email']
        password = request.POST['password']
        confirmacion = False
        try:
            lista_usuario.agrega_Lista(nombre, password)
            cadena = lista_usuario.cadena_Dot()
            print("-----------Registrando en CALENDAR------------")
            print("Usuario: "+nombre)
            print("Password: "+password)
            print("-----------Fin Registro CALENDAR------------")
            log_de_cambios("| Registro de Usuario en Calendar (Web): "+nombre+" |")
            confirmacion = True
        except Exception as inst:
            confirmacion = False
            print("Error en el registro en Drive en Views_C.Py")
    return render(request, 'Registro_Calendar.html',{'confirmacion': confirmacion})

def log_in_usuarios(request):
    if request.method == 'POST':
        nombre = request.POST['email']
        password = request.POST['password']
        try:
            resp = lista_usuario.log_in_check(nombre, password)
            if resp == "True":
                print("--------------LOG IN CHECK-------------TRUE---CALENDAR")
                request.session['usuario'] = nombre
                log_de_cambios("| Inicio de Sesión Calendar (Web): "+nombre+" |\n")
                return render(request,'Calendar/Calendario.html')
            else:
                invalido = True
                print("--------------LOG IN CHECK-------------FALSE---CALENDAR")
                log_de_cambios("| Inicio de Sessión Fallido Calendar (Web): "+nombre+" |\n")
                return render(request, 'LogIn_Calendar.html',{'invalido':invalido})
        except Exception as er:
            print("Error en el log in en Calendar en Views_C.py "+str(er))
    else:
        return HttpResponse("ruta solo de POST")

def log_de_cambios(cambio):
    try:
        bitacora_cambios_c.inserta_lista(cambio)
        print("----------------------CALENDAR-CAMBIO-ALMACENADO-----------")
    except Exception as err:
        print("Error al ingresar un cambio hecho en Calendar, log_de_cambios, views_C.py "+str(err))

# FUNCIONES PARA MANEJAR EL INGRESO DE DATOS EN LAS ESTRUCTURAS DESDE ANDROID CALENDAR

@csrf_exempt
def registro_usuarios_android(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        password = request.POST['contraseña']
        try:
            lista_usuario.agrega_Lista(nombre, password)
            print("-----------Registrando en CALENDAR DESDE ANDROID------------")
            print("Usuario: "+nombre)
            print("Password: "+password)
            print("-----------Fin Registro CALENDAR DESDE ANDROID------------")
            log_de_cambios("| Registro de Usuario en Calendar (Android): "+nombre+" |\n")
            return HttpResponse("registrado")
        except Exception as err:
            print("Error en el registro de Usuarios desde Android para Calendar, views_C.py"+str(err))
            return HttpResponse("no registrado")
    else:
        return HttpResponse("no registrado")

@csrf_exempt
def log_in_usuarios_Android(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        password = request.POST['contraseña']
        try:
            resp = lista_usuario.log_in_check(nombre, password)
            if resp == "True":
                print("--------------LOG IN CHECK ANDROID-------------TRUE")
                log_de_cambios("| Inicio de Sesión Calendar (Android): "+nombre+" |\n")
                return HttpResponse("valido")
            else:
                print("--------------LOG IN CHECK ANDROID------------FALSE")
                log_de_cambios("| Inicio de Sessión Fallido Calendar (Android): "+nombre+" |\n")
                return HttpResponse("invalido")
        except Exception as inst:
            print("Error en el log in de Android para Calendar, en Views_C.py"+str(inst))
            return HttpResponse("invalido")