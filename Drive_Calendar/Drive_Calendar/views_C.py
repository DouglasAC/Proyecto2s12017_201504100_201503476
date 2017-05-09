from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt #Utilizo este import para hacer que ciertas urls no tengan protección por csrf
from Drive_Calendar.Calendar_EDD import Lista
from Drive_Calendar.Calendar_EDD import Bitacora
from django.http import HttpResponse
import json

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
@csrf_exempt
def reporte_matriz(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        try:
            matriz = lista_usuario.buscar_matriz_usuario(usuario)
            cadena = matriz.cadena_DOT()
            return HttpResponse(cadena)
        except Exception as error:
            print("ERROR en reporte de matriz: "+str(error))
    else:
        return HttpResponse("ERROR")
@csrf_exempt
def reporte_hash(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        year = request.POST['year']
        month = request.POST['month']
        day = request.POST['day']
        try:
            matriz = lista_usuario.buscar_matriz_usuario(usuario)
            if matriz is not None:
                nodo_existe = matriz.buscar_nodo(year, month, day)
                if nodo_existe is not None:
                    cadena = nodo_existe.tabla.reporteHash()
                else:
                    cadena = "<h1>ESTA NULO NO EXISTE</h1>"
            else:
                cadena = "<h1>error</h1>"
        except Exception as error:
            print("Error: "+str(error))
            cadena = "<h1>"+str(error)+"</h1>"
    return HttpResponse(cadena)

# FUNCIONES PARA MANEJAR EL REDIRECCIONAMIENTO ENTRE PAGINAS CALENDAR
def log_In_view(request):

    return render(request, 'LogIn_Calendar.html')

def reg_view(request):

    return render(request, 'Registro_Calendar.html')

def view_crear_eventos(request):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Semptiembre', 'Octubre', 'Noviembre', 'Diciembre']
    dias = list()
    years = list()
    for x in range(1,31):
        dias.append(x)
    for x in range(1900, 2050):
        years.append(x)
    if request.method == 'POST':
        return render(request, 'Calendar/AddEvento.html',{'meses':meses, 'dias':dias, 'years':years})
    else:
        return render(request, 'Calendar/AddEvento.html',{'meses':meses, 'dias':dias, 'years':years})
        
            
        

# FUNCIONES PARA MANEJAR EL INGRESO DE DATOS EN CALENDAR

def registro_usuarios(request):
    if request.method == 'POST':
        nombre = request.POST['email']
        password = request.POST['password']
        confirmacion = False
        if lista_usuario.existe_usuario(nombre) == "False":
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

def ingresar_Evento(request):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Semptiembre', 'Octubre', 'Noviembre', 'Diciembre']
    dias = list()
    years = list()
    for x in range(1,31):
        dias.append(x)
    for x in range(1900, 2050):
        years.append(x)
    if request.method == 'POST':
        usuario = request.POST['usuario']
        day = request.POST['day']
        print(day)
        month = request.POST['month']
        print(month)
        year = request.POST['year']
        print(year)
        nombre = request.POST['nombre']
        descrip = request.POST['descrip']
        direrc = request.POST['direc']
        #hora = request.POST['hora']
        hora = ""
        confirmacion = False
        try:
            matriz = lista_usuario.buscar_matriz_usuario(usuario)
            if matriz is not None:
                nodo_existe = matriz.buscar_nodo(year, month, day)
                if nodo_existe is not None:
                    fecha = day+"/"+month+"/"+year
                    print("esta fecha: "+fecha)
                    nodo_existe.tabla.insertar(nombre, direrc, fecha, descrip, hora)
                    confirmacion = True
                    return render(request, 'Calendar/AddEvento.html', {'meses':meses, 'dias':dias, 'years':years, 'confirmacion': confirmacion})
                else:
                    print("esta fecha no existe")
                    matriz.ingresar_matriz(year, month, day, nombre, descrip, direrc, hora)
                    confirmacion = True
                    return render(request, 'Calendar/AddEvento.html', {'meses':meses, 'dias':dias, 'years':years, 'confirmacion': confirmacion})
            else:
                return HttpResponse("la matriz del usuario es nula")
        except Exception as error:
            confirmacion = False
            print("error en ingresar a matriz "+str(error))
            return render(request, 'Calendar/AddEvento.html', {'meses':meses, 'dias':dias, 'years':years, 'confirmacion': confirmacion})
    else:
        return HttpResponse("error")

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

@csrf_exempt
def prueba(request):
    if request.method == 'POST':
        nuevo1 = persona("Ricardo", "20")
        nuevo2 = persona("Chris", "20")
        lista = list()
        lista.append(nuevo1)
        lista.append(nuevo2)
        serializar = json.dumps(lista, cls = UserEncoder, indent=4)
        return HttpResponse(str(serializar))
    else:
        return HttpResponse("hola")

@csrf_exempt
def eventos_android(request):
    usuario = request.POST['usuario']
    fecha = request.POST['fecha']
    lista = fecha.split("-")
    dia = lista[0]
    mes = lista[1]
    year = lista[2]
    nombre = request.POST['nombre']
    descrip = request.POST['descrip']
    direrc = request.POST['direc']
    hora = request.POST['hora']
    print(hora)
    print(fecha)
    try:
        matriz = lista_usuario.buscar_matriz_usuario(usuario)
        if matriz is not None:
            nodo_existe = matriz.buscar_nodo(year, mes, dia)
            if nodo_existe is not None:
                fecha2 = dia+"/"+mes+"/"+year
                nodo_existe.tabla.insertar(nombre, direrc, fecha2, descrip, hora)
                confirmacion = True
                return HttpResponse("SI")
            else:
                matriz.ingresar_matriz(year, mes, dia, nombre, descrip, direrc, hora)
                return HttpResponse("SI")
        else:
            return HttpResponse("la matriz del usuario es nula")
    except Exception as err:
        print("err: "+str(err))
    return HttpResponse("hola")


class persona:
    
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

class UserEncoder(json.JSONEncoder):

    def default(self, obj):
        return obj.__dict__