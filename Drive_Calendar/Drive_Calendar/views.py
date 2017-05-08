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
@csrf_exempt
def conAndroid(request):
    if request.method == 'POST':
        return HttpResponse("<h1>esta conectado</h1>")
    else:
        return HttpResponse("<h1>esta GET</h1>")
def Conectar(request):
    return HttpResponse("Conexion Correcta con Java y Django")

def reporte_usuarios(request):
    cadena = lista_usuario.cadena_Dot()
    return HttpResponse(cadena)

def reporte_bitacora(request):
    cadena = bitacora_cambios.listar_bitadora()
    return HttpResponse("| Historial de Drive |\n"+cadena)

@csrf_exempt
def reporte_directorio(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        path = request.POST['path']
        cadena = ""
        try:
            carp = path.split("/")
            dir = lista_usuario.obtener_directorio(nombre)
            if path == "":
                cadena = dir.imprimir_arbol()
            else:
                arbol = lista_usuario.buscar_arbo(dir, carp)
                cadena = arbol.imprimir_arbol()
        except Exception as err:
            print("Error... "+str(err))
            cadena = "vacio..."
        return HttpResponse(cadena)
@csrf_exempt
def reporte_avl(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        path = request.POST['path']
        cadena = ""
        if path == "":
            try:
                Avl = lista_usuario.obtener_archivos(usuario)
                cadena = Avl.graficar()
            except Exception as error:
                print("erro: "+str(error))
        else:
            try:
                listadocarpetas = path.split("/")
                dir = lista_usuario.obtener_directorio(usuario)
                nodoaux = lista_usuario.buscar_avl(dir, listadocarpetas)
                cadena = nodoaux.files.graficar()
            except Exception as err:
                print("error: "+str(err))
    return HttpResponse(cadena)

# FUNCIONES PARA MANEJAR EL REDIRECCIONAMIENTO ENTRE PAGINAS DRIVE
def index(request):    
    return render(request, 'index.html')

def LogInView(request):

    return render(request, 'LogIn.html')

def Registro(request):

    return render(request, 'Registro.html')

def add_folder(request):
    return render(request, 'Drive/AddCarpetas.html')

def listar_folder_path(request):
    if request.method == 'POST':
        nombre = request.POST['user']
        path = request.POST['path']
        carpetas = None
        if path == "":
            dir = lista_usuario.obtener_directorio(nombre)
            carpetas = dir.listar_string()
        else:
            carp = path.split("/")
            dir = lista_usuario.obtener_directorio(nombre)
            arbol = lista_usuario.buscar_arbo(dir, carp)
            carpetas = arbol.listar_string()
        return render(request, 'Drive/Editar_C.html', {'carpetas':carpetas, 'path': path})
    else:
        if request.session['usuario'] is not None:
            dir = None
            dir = lista_usuario.obtener_directorio(request.session['usuario'])
            carpetas = dir.listar_string()
            return render(request, 'Drive/Editar_C.html',{'carpetas': carpetas, 'path': '/'})

def editar_folder_path(request, path):
    if request.method == 'POST':
        return HttpResponse("POST "+path)
    else:
        return HttpResponse("GET "+path)
def vista_upload(request):
    return render(request, 'Drive/AddFile.html')

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
                dir = lista_usuario.obtener_directorio(nombre)
                carpetas = dir.listar_string()
                log_de_cambios_drive("| Inicio de Sesión Drive (Web): "+nombre+" |\n")
                return render(request, 'Drive/Menu.html', {'carpetas': carpetas})
            else:
                salida = "Datos Incorrectos"
                invalido = True
                print("------------LOG IN CHECK --------FALSE")
                log_de_cambios_drive("| Inicio de Sessión Fallido Drive (Web): "+nombre+" |\n")
                return render(request, 'LogIn.html', {'invalido':invalido})
        except Exception as inst:
            print("Error en el log in en Dirve en Views.py"+str(inst))
    else:
        if request.session['usuario'] is not None:
            nombre = request.session['usuario']
            dir = lista_usuario.obtener_directorio(nombre)
            carpetas = dir.listar_string()
            return render(request, 'Drive/Menu.html', {'carpetas': carpetas})
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
        carpetas = ""
        clave = request.POST['clave']
        nombre = request.POST['nombre']
        path = request.POST['path']
        resp = ""
        if path == "":
            resp = lista_usuario.usuario_agregar_carpeta(nombre, clave)
            log_de_cambios_drive("| Creación de Carpeta: "+clave+" en Path: /"+path+" Por Usuario: "+nombre+" |")
        else:
            carpetas = path.split("/")
            x = len(carpetas)-1
            nueva = carpetas[x]
            #print(carpetas)
            dir = lista_usuario.obtener_directorio(nombre)
            arbol_cor = lista_usuario.buscar_arbo(dir, carpetas)
            try:
                arbol_cor.insertar(clave)
                cad = arbol_cor.imprimir_arbol()
                log_de_cambios_drive("| Creación de Carpeta: "+clave+" en Path: /"+path+" Por Usuario: "+nombre+" |")
            except Exception as error:
                print("El arbol es nulo... "+str(error))
                log_de_cambios_drive("| Error en creación de Carpeta: "+clave+" en Path: /"+path)
            #print(cad)
            resp = "hecho"
        #print(path)
        #resp = lista_usuario.usuario_agregar_carpeta(nombre, clave)
        #resp = lista_usuario.carpetas_path(carp, nombre, clave)
        #print(carp)
        #print(nombre)
        #print(clave)
        #print(resp)
        if resp == "hecho":
            #print("creada con exito")
            return HttpResponse("Carpeta Creada Con Éxito!")
        elif resp == "duplicado":
            return HttpResponse("la carpeta ya existe...")
        else:
            return HttpResponse("No se loró crear la carpeta"+ nombre)
    else:
        return HttpResponse("invalido")

def new_file(request):
    if request.method == 'POST':
        confirm = False
        arch = request.FILES['archi']
        path = request.POST['path']
        usuario = request.POST['nombre']
        fs = FileSystemStorage()
        nombrefile = fs.save(arch.name, arch)
        upload_dir = fs.url(nombrefile)
        ruta = settings.BASE_DIR+"\\media\\"+nombrefile
        archivo = lista_usuario.leer_archivo(ruta)
        lista = ruta.split("\\")
        x = len(lista) - 1
        nombre = lista[x]
        lista2 = nombre.split(".")
        extension = lista2[1]
        name = lista2[0]
        if path == "":
            Avl = lista_usuario.obtener_archivos(usuario)
            try:
                print("entro aqui porque path es vacio")
                Avl.agregar(name, extension, archivo)
                cadena = Avl.graficar()
                confirm = True
                print(cadena)
            except Exception as r:
                confirm = False
                print("error... "+str(r))
        else:
            print("entro cuando hay una carpeta")
            listadocarpetas = path.split("/")
            dir = lista_usuario.obtener_directorio(usuario)
            nodoaux = lista_usuario.buscar_avl(dir, listadocarpetas)
            try:
                nodoaux.files.agregar(nombre, extension, archivo)
                cadena = nodoaux.files.graficar()
                confirm = True
                print(cadena)
            except Exception as err:
                confirm = False
                print("Error "+str(err))
        return render(request, 'Drive/AddFile.html', {'confirm':confirm})
        

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
        #arc = request.POST['pr']
        fs = FileSystemStorage()
        filena = fs.save(filename.name, filename)
        uploaded_file_url = fs.url(filena)
        #print(arc)
        #print(uploaded_file_url)
    return HttpResponse("file: "+settings.BASE_DIR+"\\media\\"+str(filename))

def file_view(request):
    return render(request,'pr.html')