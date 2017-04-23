from django.shortcuts import render
from django.http import HttpResponse
from Drive_Calendar.Drive_EDD import Lista

# ESTRUCTURAS DRIVE
lista_usuario = Lista.ListaDoble()

#CONEXION CON JAVA Y REPORTES DE DRIVE
def Conectar(request):
    return HttpResponse("Conexion Correcta con Java y Django")

def reporte_usuarios(request):
    cadena = lista_usuario.cadena_Dot()
    return HttpResponse(cadena)

# FUNCIONES PARA MANEJAR EL REDIRECCIONAMIENTO ENTRE PAGINAS DRIVE
def index(request):

    return render(request, 'index.html')

def LogInView(request):

    return render(request, 'LogIn.html')

def Registro(request):

    return render(request, 'Registro.html')

# FUNCIONES PARA MANEJAR EL INGRESO DE DATOS EN LAS ESRUCTURAS DESDE WEB DRIVE

def registro_usuarios_web(request):
    if request.method == "POST":
        nombre = request.POST['email']
        password = request.POST['password']
        try:
            lista_usuario.agrega_Lista(nombre, password)
            cadena = lista_usuario.cadena_Dot()
            print("-----------Registrando en DRIVE------------")
            print("Usuario: "+nombre)
            print("Password: "+password)
            print("-----------Fin Registro DRIVE------------")
        except Exception as inst:
            print("Error en el registro en Drive en Views.Py")        
    return render(request, 'pr.html',{'var': cadena})

def log_in_usuarios_web(request):
    if request.method == 'POST':
        nombre = request.POST['email']
        password = request.POST['password']
        salida = ""
        try:
            resp = lista_usuario.log_in_check(nombre, password)
            if resp == "True":
                salida = "Acceso Concedido a: "+nombre
                print("--------------LOG IN CHECK-------------TRUE")
            else:
                salida = "Datos Incorrectos"
                print("------------LOG IN CHECK --------FALSE")
        except Exception as inst:
            print("Error en el log in en Dirve en Views.py")
    return render(request, 'pr.html',{'var':salida})

# FUNCIONES PARA MANEJAR EL INGRESO DE DATOS EN LAS ESTRUCTURAS DESDE ANDROID DRIVE