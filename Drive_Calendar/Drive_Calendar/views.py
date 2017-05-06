from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt #Utilizo este import para hacer que ciertas urls no tengan protección por csrf
from Drive_Calendar.Drive_EDD import Lista
from Drive_Calendar.Drive_EDD import Bitacora
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# ESTRUCTURAS DRIVE
lista_usuario = Lista.ListaDoble()
bitacora_cambios = Bitacora.Bitacora()

#CONEXION CON JAVA Y REPORTES DE DRIVE
def Conectar(request):
    return HttpResponse("Conexion Correcta con Java y Django")

def reporte_usuarios(request):
    cadena = lista_usuario.cadena_Dot()
    return HttpResponse(cadena)

def reporte_bitacora(request):
    cadena = bitacora_cambios.listar_bitadora()
    return HttpResponse("| Historial de Drive |\n"+cadena)

# FUNCIONES PARA MANEJAR EL REDIRECCIONAMIENTO ENTRE PAGINAS DRIVE
def index(request):

    return render(request, 'index.html')

def LogInView(request):

    return render(request, 'LogIn.html')

def Registro(request):

    return render(request, 'Registro.html')

def add_folder(request):
    return render(request, 'Drive/AddCarpetas.html')
# FUNCIONES PARA MANEJAR EL INGRESO DE DATOS EN LAS ESRUCTURAS DESDE WEB DRIVE

def registro_usuarios_web(request):
    if request.method == "POST":
        nombre = request.POST['email']
        password = request.POST['password']
        confirmacion = False
        if lista_usuario.existe_usuario(nombre) == "False":  
            try:
                lista_usuario.agrega_Lista(nombre, password)
                cadena = lista_usuario.cadena_Dot()
                confirmacion = True
                print("-----------Registrando en DRIVE------------")
                print("Usuario: "+nombre)
                print("Password: "+password)
                print("-----------Fin Registro DRIVE------------")
                log_de_cambios_drive("| Registro de Usuario en Drive (Web): "+nombre+" |")
            except Exception as inst:
                confirmacion = False
                print("Error en el registro en Drive en Views.Py")        
    return render(request, 'Registro.html',{'confirmacion': confirmacion})

def log_in_usuarios_web(request):
    if request.method == 'POST':
        nombre = request.POST['email']
        password = request.POST['password']
        salida = ""
        try:
            resp = lista_usuario.log_in_check(nombre, password)
            if resp == "True":
                salida = "Acceso Concedido a: "+nombre
                request.session['usuario'] = nombre
                print("--------------LOG IN CHECK-------------TRUE")
                log_de_cambios_drive("| Inicio de Sesión Drive (Web): "+nombre+" |\n")
                return render(request, 'Drive/Menu.html')
            else:
                salida = "Datos Incorrectos"
                invalido = True
                print("------------LOG IN CHECK --------FALSE")
                log_de_cambios_drive("| Inicio de Sessión Fallido Drive (Web): "+nombre+" |\n")
                return render(request, 'LogIn.html', {'invalido':invalido})
        except Exception as inst:
            print("Error en el log in en Dirve en Views.py"+str(inst))
    #return render(request, 'pr.html',{'var':salida})
def guardar_cambios(request):
    if request.method == 'GET':
        cambio = request.POST['cambio']
        try:
            bitacora_cambios.inserta_lista(cambio)
            print("|-------------Bitacora Actual---------------|")
            salida = "|-------------Bitacora Actual---------------|\n"
            salida = salida + bitacora_cambios.listar_bitadora()+"\n"
            salida = salida + "|-------------Fin---------------|"
            print(salida)
            print("|-------------Fin Bitacora---------------|")
            return HttpResponse(salida)
        except Exception as err:
            print("Error Al registrar el cambio")
    else:
        return HttpResponse("Esta es solo una ruta GET")

def log_de_cambios_drive(cambio):
    try:
        bitacora_cambios.inserta_lista(cambio)
        print("----------------------DRIVE-CAMBIO-ALMACENADO-----------")
    except Exception as err:
        print("Error en Views.py en log_cambios_drive "+str(err))

def new_folder(request):
    if request.method == "POST":
        clave = request.POST['clave']
        nombre = request.POST['nombre']
        resp = lista_usuario.usuario_agregar_carpeta(nombre, clave)
        #print(nombre)
        #print(clave)
        #print(resp)
        if resp == "creado":
            #print("creada con exito")
            return HttpResponse("Carpeta Creada Con Éxito!")
        elif resp == "duplicado":
            return HttpResponse("la carpeta ya existe...")
        else:
            return HttpResponse("No se loró crear la carpeta"+ nombre)
    else:
        return HttpResponse("invalido")


# FUNCIONES PARA MANEJAR EL INGRESO DE DATOS EN LAS ESTRUCTURAS DESDE ANDROID DRIVE

@csrf_exempt
def registro_usuarios_android(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        password = request.POST['contraseña']
        try:
            lista_usuario.agrega_Lista(nombre, password)
            print("-----------Registrando en DRIVE DESDE ANDROID------------")
            print("Usuario: "+nombre)
            print("Password: "+password)
            print("-----------Fin Registro DRIVE DESDE ANDROID------------")
            log_de_cambios_drive("| Registro de Usuario en Drive (Android): "+nombre+" |\n")
            return HttpResponse("registrado")
        except Exception as inst:
            print("Error en el registro de Usuarios desde Android para Drive, views.py "+str(inst))
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
                log_de_cambios_drive("| Inicio de Sesión Drive (Android): "+nombre+" |\n")
                return HttpResponse("valido")
            else:
                print("--------------LOG IN CHECK ANDROID------------FALSE")
                log_de_cambios_drive("| Inicio de Sessión Fallido Drive (Android): "+nombre+" |\n")
                return HttpResponse("invalido")
        except Exception as inst:
            print("Error en el log in de Android para Drive, en Views.py"+str(inst))
            return HttpResponse("invalido")

#ESTOS METODOS SON DE PRUEBA PARA ARCHIVOS
def file_upload(request):
    if request.method == 'POST':
        filename = request.FILES['pr']
        arc = request.POST['pr']
        fs = FileSystemStorage()
        filena = fs.save(filename.name, filename)
        uploaded_file_url = fs.url(filena)
        print(arc)
    return HttpResponse("file: "+settings.BASE_DIR+"\\media\\"+str(filename))

def file_view(request):
    return render(request,'pr.html')