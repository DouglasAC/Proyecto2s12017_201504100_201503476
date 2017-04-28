class NodoLista:
    def __init__(self, cambio):
        self.cambio = cambio
        self.siguiente = None

class Bitacora:

    def __init__(self):
        self.cabeza = None
        self.ultimo = None
    
    def esta_vacia(self):
        if self.cabeza == None:
            return True
        else:
            return False
    
    def inserta_lista(self, cambio):
        nuevo = NodoLista(cambio)
        if self.esta_vacia() == True:
            try:
                self.cabeza = nuevo
                self.ultimo = nuevo
                #self.cabeza.siguiente = self.ultimo
            except Exception as error:
                print("Error en insertar Lista: "+ str(error))            
        else:
            try:
                self.ultimo.siguiente = nuevo
                self.ultimo = nuevo
            except Exception as error:
                print("Error en insertar lista: "+str(error))

    def listar_bitadora(self):
        if self.esta_vacia() == True:
            return "Bitácora sin cambios"
        else:
            retorno = ""
            aux = self.cabeza
            while aux is not None:
                retorno = retorno + " | "+ str(aux.cambio)+ " | \n"
                aux = aux.siguiente
            return retorno
