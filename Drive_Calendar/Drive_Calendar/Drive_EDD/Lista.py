# LISTA DE USUARIOS DE DRIVE
from Drive_Calendar.Drive_EDD import Carpetas
class Usuario:
    
    def __init__(self, nombre, password):
        self.nombre = nombre
        self.password = password
        self.dir = Carpetas.ArbolB()

    def __str__(self):
        pass

class NodoLista:

    def __init__(self, usuario):
        self.siguiente = None
        self.anterior = None
        self.usuario = usuario

class ListaDoble:

    raiz = NodoLista(None)
    node = raiz

    def __init__(self):
        self.raiz = None

    def esta_vacia(self):
        if self.raiz is None:
            return True
        else:
            return False

    def agrega_Lista(self, nombre, password):
        # Añadiendo nuevo usuario a la Lista
        nuevo_us = Usuario(nombre, password)
        nuevo_nodo = NodoLista(nuevo_us)
        # Si la lista esta vacía lo inserta en la raíz
        if self.esta_vacia() is True:
            try:
                self.raiz = nuevo_nodo
                self.node = self.raiz
            except Exception as ex:
                print("Error al Empezar a llenar la Lista: raiz: "+ ex)
        else:
            # de lo contrario recorre la lista para insertarlo al final
            aux = self.raiz
            while aux.siguiente is not None:
                try:
                    aux = aux.siguiente
                except Exception as inst:
                    print("Error al recorrer la lista: "+inst)
            try:
                aux.siguiente = nuevo_nodo
                nuevo_nodo.anterior = aux
            except Exception as inst:
                print("error al recorrer al insertar en Lista "+inst)
    
    def imprimir_lista(self):
        aux = self.raiz
        print("---------Inicio de Lista---------")
        while aux is not None:
            print("Usuario: "+ aux.usuario.nombre)
            aux = aux.siguiente
        print("---------Fin de Lista-----------")
    
    def cadena_Dot(self):
        aux = self.raiz
        cadena = "digraph G{\n"
        while aux is not None:
            if aux.siguiente is not None:
                cadena = cadena + '"'+aux.usuario.nombre+'" -> '+ '"'+aux.siguiente.usuario.nombre+'";\n'
                cadena = cadena + '"'+aux.siguiente.usuario.nombre+'" -> '+ '"'+aux.usuario.nombre+'";\n'
            else:
                cadena = cadena + '"'+aux.usuario.nombre+'";\n'
            if aux.siguiente is not None:
                aux = aux.siguiente
            else:
                break
        cadena = cadena + "}"
        return cadena
    
    def log_in_check(self, nombre, password):
        aux = self.raiz
        bandera = "False"
        while aux is not None:
            try:
                if aux.usuario.nombre == nombre and aux.usuario.password == password:
                    bandera = "True"
                    break
                if aux.siguiente is not None:
                    aux = aux.siguiente
                else:
                    break
            except Exception as inst:
                print("Ocurrio un error al buscar... en Drive log_in_check")
        return bandera
    
    def existe_usuario(self, nombre):
        aux = self.raiz
        bandera = "False"
        while aux is not None:
            try:
                if aux.usuario.nombre == nombre:
                    bandera = "True"
                    break
                if aux.siguiente is not None:
                    aux = aux.siguiente
                else:
                    break
            except Exception as err:
                print("Error en el checkeo de Usuario: existe_usuario "+ str(err))
        return bandera
    
    def accdeder_directorio(self, nombre):
        aux = self.raiz
        directorio_aux = Carpetas.ArbolB()
        while aux is not None:
            try:
                if aux.usuario.nombre == nombre:
                    directorio_aux = aux.usuario.dir
                    break
                if aux.siguiente is not None:
                    aux = aux.siguiente
                else:
                    break
            except Exception as err:
                print("Error al acceder al directorio")
        return directorio_aux
    
    def usuario_agregar_carpeta(self, nombre, carpeta):
        aux = self.raiz
        resp = ""
        print(carpeta)
        directorio_aux = Carpetas.ArbolB()
        while aux is not None:
            try:
                if aux.usuario.nombre == nombre:
                    #print("encontre: "+str(aux.usuario.nombre))
                    directorio_aux = aux.usuario.dir
                    break
                if aux.siguiente is not None:
                    aux = aux.siguiente
                else:
                    break
            except Exception as err:
                print("Error al acceder al directorio")
                resp = "Error al acceder al dir"
        if aux.usuario.dir is not None:
            auxlista = aux.usuario.dir.listar_string()
            #print(cad)
            #print(auxlista)
            #print(carpeta)
            #print(carpeta in auxlista)
            if (carpeta in auxlista) == False:
                aux.usuario.dir.insertar(carpeta)
                resp = "hecho"
            else:
                resp = "duplicado"
        auxlista = aux.usuario.dir.listar_string()
        cad = aux.usuario.dir.imprimir_arbol()
        #aux.usuario.dir.print_root()
        #print(cad)
        print(auxlista)
        #print(resp)
        return resp
    
    def obtener_directorio(self, nombre):
        aux = self.raiz
        while aux is not None:
            try:
                if aux.usuario.nombre == nombre:
                    dir = aux.usuario.dir
                    break
                if aux.siguiente is not None:
                    aux = aux.siguiente
                else:
                    break
            except Exception as err:
                print("err: "+str(err))
        return dir
    
    def verLista(self, dir):
        lista = dir.listar_carpetas()
        print(lista)
    
    def buscar_arbo(self, dir, listacarpetas):
        return self.buscar_arbol_correcto(dir, listacarpetas)
    
    def buscar_arbol_correcto(self, dir, listacarpetas):
        listado_obj = dir.listar_carpetas() #obtengo los objetos carpetas
        buscar = "" #carpeta a buscar
        nodo_retorna = None
        if len(listacarpetas) > 0:
            buscar = listacarpetas.pop(0)
        for cada_carp in listado_obj:
            if cada_carp.clave == buscar:
                nodo_retorna = cada_carp.sub_carp
                break
        if len(listacarpetas)>0:
            print("recurividad")
            return self.buscar_arbol_correcto(nodo_retorna, listacarpetas)
        else:
            print("retorno nodo")
            return nodo_retorna
