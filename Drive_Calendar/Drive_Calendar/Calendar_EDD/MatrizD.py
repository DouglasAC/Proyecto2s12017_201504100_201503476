from Drive_Calendar.Calendar_EDD import NodoEvento
from Drive_Calendar.Calendar_EDD import TablaHash
class Evento:
    
    def __init__(self, nombre, descrip):
        self.nombre = nombre
        self.descrip = descrip

class Nodo:

    def __init__(self):
        #hace falta hash
        self.month = ""
        self.year = ""
        self.day = ""
        self.tabla = TablaHash.TablaHash()
        self.evento = None
        self.arriba = None
        self.abajo = None
        self.anterior = None
        self.siguiente = None
        self.atras = None
        self.adelante = None

class Matriz:
    
    raiz = Nodo()
    #node = raiz
    esta3D = False
    puntero3D = Nodo()

    #Constructor de Matriz
    def __init__(self):
        self.raiz.month = "Raiz"
        self.raiz.year = "Raiz"
        self.raiz.day = "Raiz"
        self.node = self.raiz
    
    # verifica si la matriz esta vacia
    def matriz_vacia(self):
        if self.raiz.siguiente is None or self.raiz.abajo is None:
            return True
        else:
            return False
    
    #numero de datos en columnas
    def numero_datos_columnas(self, nodoB):
        aux = nodoB
        contador = -1
        while aux is not None:
            aux = aux.abajo
            contador = contador+1
        return contador
    
    #retorna numero de datos en filas
    def numero_datos_fila(self, nodoB):
        aux = nodoB
        contador = 0
        while aux is not None:
            if aux.siguiente is not None:
                aux = aux.siguiente
            else:
                break
            contador = contador+1
        return contador
    
    #eliminar punteros desde fila
    def puntero_eliminar_desde_fila(self, nodoB, day, month, year):
        aux = nodoB
        while aux is not None:
            if aux.day == day and aux.month == month and aux.year == year:
                break
            else:
                if aux.adelante is not None:
                    pass
                    self.puntero3D = self.puntero_eliminar_3D(aux, day, month, year)
            aux = aux.siguiente
        return aux
    
    #eliminar desde columna
    def puntero_elimnar_desde_colum(self, nodoB, day, month, year):
        aux = nodoB
        while aux is not None:
            if aux.day == day and aux.year == year and aux.month == month:
                break
            else:
                pass
                if aux.adelante is not None:
                    self.puntero3D = self.puntero_eliminar_3D(aux, day, month, year)
            aux = aux.siguiente
        return aux
    
    #eliminar en 3D
    def puntero_eliminar_3D(self, nodoB, day, month, year):
        aux1 = nodoB.adelante
        while aux1 is not None:
            if aux1.day == day and aux1.month == month and aux1.year == year:
                self.esta3D = True
                break
            aux1 = aux1.adelante
        return aux1
    
    #Metodo que verifica si existe columna
    def existe_columna(self, year):
        bandera = False
        aux_col = self.raiz.siguiente
        while aux_col is not None:
            if aux_col.year == year:
                bandera = True
                break
            aux_col = aux_col.siguiente
        return bandera

    #Metodo que verifica si existe fila
    def existe_fila(self, month):
        bandera = False
        aux_fil = self.raiz.abajo
        while aux_fil is not None:
            if aux_fil.month == month:
                bandera = True
                break
            aux_fil = aux_fil.abajo
        return bandera
    
    #Crea las cabeceras de los años
    def crear_cabeceras_year(self, year):
        aux = self.raiz.siguiente
        nuevo = Nodo()
        nuevo.month = year
        nuevo.year = year
        nuevo.day = year
        bandera = 0
        if self.matriz_vacia() is True:
            try:
                self.raiz.siguiente = nuevo
                nuevo.anterior = self.raiz
            except Exception as er:
                print("Error: crear_cabeceras_year: "+str(er))
            return nuevo
        else:
            try:
                while aux is not None:
                    if year < aux.year:
                        bandera = 1
                        break
                    if aux.siguiente is not None:
                        aux = aux.siguiente
                    else:
                        break
                if bandera == 1:
                    aux.anterior.siguiente = nuevo
                    nuevo.anterior = aux.anterior
                    nuevo.siguiente = aux
                    aux.anterior = nuevo
                if bandera == 0:
                    aux.siguiente = nuevo
                    nuevo.anterior = aux
            except Exception as er:
                print("Error: crear_cabeceras_year: "+str(er))
        return nuevo
    
    #crear las cabecereas de los meses
    def crear_cabeceras_month(self, month):
        bandera = 0
        auxiliar = self.raiz.abajo
        nuevo = Nodo()
        nuevo.year = month
        nuevo.month = month
        nuevo.day = month
        if self.matriz_vacia() is True:
            self.raiz.abajo = nuevo
            nuevo.arriba = self.raiz
        else:
            while auxiliar is not None:
                try:
                    if month < auxiliar.month:
                        bandera = 1
                        break
                    if auxiliar.abajo is not None:
                        auxiliar = auxiliar.abajo
                    else:
                        break
                except Exception as err:
                    print("Error: crear_cabeceras_month: "+str(err))
            if bandera == 1:
                try:
                    auxiliar.arriba.abajo = nuevo
                    nuevo.arriba = auxiliar.arriba
                    nuevo.abajo = auxiliar
                    auxiliar.arriba = nuevo
                except Exception as err:
                    print("Error: crear_cabeceras_month: "+str(err))
            if bandera == 0:
                try:
                    auxiliar.abajo = nuevo
                    nuevo.arriba = auxiliar
                except Exception as err:
                    print("Error: crear_cabeceras_month: "+str(err))
        return nuevo
    
    #INGRESAR VA AQUI....
    def ingresar_matriz(self, year, month, day, nombre, descrip, direccion, hora):
        nuevo = Nodo()
        nuevo.year = year
        nuevo.month = month
        nuevo.day = day
        fecha = day+"/"+month+"/"+year
        nuevo.tabla.insertar(nombre, direccion, fecha, descrip, hora)
        existe_col = self.existe_columna(year)
        existe_fil = self.existe_fila(month)
        if existe_col is False and existe_fil is False:
            try:
                print("Primer caso")
                puntero_colum = self.crear_cabeceras_year(year)
                puntero_fil = self.crear_cabeceras_month(month)
                puntero_colum.abajo = nuevo
                nuevo.arriba = puntero_colum
                puntero_fil.siguiente = nuevo
                nuevo.anterior = puntero_fil
                return None
            except Exception as err:
                print("Ing a Matriz Primer Caso: "+str(err))
                return None
        if existe_col is False and existe_fil is True:
            try:
                print("Segundo Caso")
                puntero_colum = self.crear_cabeceras_year(year)
                puntero_fil = self.encuentra_fila(month)
                posicion = self.recorre_meses(puntero_fil)
                puntero_colum.abajo = nuevo
                nuevo.arriba = puntero_colum
                posicion.arriba = puntero_colum
                posicion.siguiente = nuevo
                nuevo.anterior = posicion
                return None
            except Exception as err:
                print("Ing a Matriz Segundo Caso: "+str(err))
                return None
        if existe_col is True and existe_fil is False:
            try:
                print("Tercer Caso")
                puntero_colum = self.encuentra_columna(year)
                puntero_fil = self.crear_cabeceras_month(month)
                colocado = self.recorre_columna_year(puntero_colum, nuevo)
                puntero_fil.siguiente = colocado
                colocado.anterior = puntero_fil
                return None
            except Exception as err:
                print("Ing a Matriz Tercer Caso: "+str(err))
                return None
        if existe_col is True and existe_fil is True:
            try:
                print("Cuarto Caso")
                puntero_colum = self.encuentra_columna(year)
                puntero_fil = self.encuentra_fila(month)
                colfil = self.coloca_d_fila_posicion_correcta(puntero_fil, year, nuevo)
                if colfil is not None:
                    self.coloca_d_colum_posicion_correcta(puntero_colum, colfil)
                return None
            except Exception as err:
                print("Ing a Matriz Cuarto Caso: "+str(err))
                return None      
    #ELIMINAR VA AQUI....

    def eliminar_matriz(self, year, month, day):
        puntero_col = self.encuentra_columna(year)
        puntero_fil = self.encuentra_fila(month)
        puntero_elimi = self.puntero_eliminar_desde_fila(puntero_fil, day, month, year)
        fil = self.numero_datos_fila(puntero_fil)
        col = self.numero_datos_columnas(puntero_col)
        if self.esta3D is True:
            self.esta3D = False
            self.puntero3D.atras.adelante = self.puntero3D.adelante
            if self.puntero3D.adelante is not None:
                self.puntero3D.adelante.atras = self.puntero3D.atras
            self.puntero3D.atras = None
        else:
            if fil == 1 and col == 1:
                if puntero_elimi.adelante is not None:
                    puntero_elimi.anterior.siguiente = puntero_elimi.adelante
                    puntero_elimi.arriba.abajo = puntero_elimi.adelante
                    puntero_elimi.adelante.arriba = puntero_elimi.arriba
                    puntero_elimi.adelante.anterior = puntero_elimi.anterior
                    puntero_elimi.adelante.atras = None
                    puntero_elimi.arriba = None
                    puntero_elimi.anterior = None
                    puntero_elimi.move_adelante = None
                    return None
                else:
                    puntero_col.anterior.siguiente = puntero_col.siguiente
                    if puntero_col.siguiente is not None:
                        puntero_col.siguiente.anterior = puntero_col.anterior
                    puntero_col.anterior = None
                    puntero_fil.arriba.abajo = puntero_fil.abajo
                    if puntero_fil.abajo is not None:
                        puntero_fil.abajo.arriba = puntero_fil.arriba
                    puntero_fil.arriba = None
                    return None
            if fil > 1 and col == 1:
                if puntero_elimi.adelante is not None:
                    puntero_elimi.anterior.siguiente = puntero_elimi.adelante
                    puntero_elimi.adelante.anterior = puntero_elimi.anterior
                    puntero_elimi.arriba.abajo = puntero_elimi.adelante
                    puntero_elimi.adelante.arriba = puntero_elimi.arriba
                    if puntero_elimi.siguiente is not None:
                        puntero_elimi.siguiente.anterior = puntero_elimi.adelante
                        puntero_elimi.adelante.siguiente = puntero_elimi.siguiente
                    puntero_elimi.anterior = None
                    puntero_elimi.siguiente = None
                    puntero_elimi.arriba = None
                    puntero_elimi.adelante.atras = None
                    puntero_elimi.adelante = None
                    return None
                else:
                    puntero_col.anterior.siguiente = puntero_col.siguiente
                    if puntero_col.siguiente is not None:
                        puntero_col.siguiente.anterior = puntero_col.anterior
                    puntero_col.anterior = None
                    puntero_elimi.anterior.siguiente = puntero_elimi.siguiente
                    if puntero_elimi.siguiente is not None:
                        puntero_elimi.siguiente.anterior = puntero_elimi.anterior
                    puntero_elimi.anterior = None
                    return None
            if fil == 1 and col > 1:
                if puntero_elimi.adelante is not None:
                    puntero_elimi.arriba.abajo = puntero_elimi.adelante
                    puntero_elimi.adelante.arriba = puntero_elimi.arriba
                    puntero_elimi.anterior.siguiente = puntero_elimi.move_adelante
                    puntero_elimi.adelante.anterior = puntero_elimi.anterior
                    if puntero_elimi.abajo is not None:
                        puntero_elimi.abajo.arriba = puntero_elimi.adelante
                        puntero_elimi.adelante.abajo = puntero_elimi.abajo
                    puntero_elimi.arriba = None
                    puntero_elimi.anterior = None
                    puntero_elimi.abajo = None
                    puntero_elimi.adelante.atras = None
                    puntero_elimi.adelante = None
                    return None
                else:
                    puntero_fil.arriba.abajo = puntero_fil.abajo
                    if puntero_fil.abajo is not None:
                        puntero_fil.abajo.arriba = puntero_fil.arriba
                    puntero_fil.arriba = None
                    puntero_elimi.arriba.abajo = puntero_elimi.abajo
                    if puntero_elimi.abajo is not None:
                        puntero_elimi.abajo.arriba = puntero_elimi.arriba
                    puntero_elimi.arriba = None
                    return None
            if fil > 1 and col > 1:
                if puntero_elimi.adelante is not None:
                    puntero_elimi.arriba.abajo = puntero_elimi.adelante
                    puntero_elimi.adelante.arriba = puntero_elimi.arriba
                    puntero_elimi.anterior.siguiente = puntero_elimi.adelante
                    puntero_elimi.adelante.anterior = puntero_elimi.anterior
                    if puntero_elimi.abajo is not None:
                        puntero_elimi.abajo.arriba = puntero_elimi.adelante
                        puntero_elimi.adelante.abajo = puntero_elimi.abajo
                    if puntero_elimi.siguiente is not None:
                        puntero_elimi.siguiente.anterior = puntero_elimi.adelante
                        puntero_elimi.adelante.siguiente = puntero_elimi.siguiente
                    puntero_elimi.adelante.atras = None
                    puntero_elimi.arriba = None
                    puntero_elimi.anterior = None
                    puntero_elimi.siguiente = None
                    puntero_elimi.abajo = None
                    puntero_elimi.adelante = None
                    return None
                else:
                    puntero_elimi.anterior.siguiente = puntero_elimi.siguiente
                    if puntero_elimi.siguiente is not None:
                        puntero_elimi.siguiente.anterior = puntero_elimi.anterior
                    puntero_elimi.anterior = None
                    puntero_elimi.arriba.abajo = puntero_elimi.abajo
                    if puntero_elimi.abajo is not None:
                        puntero_elimi.abajo.arriba = puntero_elimi.arriba
                    puntero_elimi.arriba = None
                    return None
                
    #metodo que encuentra fila
    def encuentra_fila(self, month):
        nodoBusca = self.raiz
        while nodoBusca is not None:
            if nodoBusca.month == month:
                break
            if nodoBusca.abajo is not None:
                nodoBusca = nodoBusca.abajo
            else:
                break
        return nodoBusca
    
    #metodo de encontrar columna
    def encuentra_columna(self, year):
        nodoBusca = self.raiz
        while nodoBusca is not None:
            if nodoBusca.year == year:
                break
            if nodoBusca.siguiente is not None:
                nodoBusca = nodoBusca.siguiente
            else:
                break
        return nodoBusca
    
    #metodo para recorrer las filas de los meses
    def recorre_meses(self, nodoB):
        retorno = None
        while nodoB.siguiente is not None:
            nodoB = nodoB.siguiente
        retorno = nodoB
        return retorno
    
    #Recorre las columnas de los años cuando la columna existe y el mes no
    def recorre_columna_year(self, nodoB, nuevo):
        bandera = 0
        retorno = None
        while nodoB.abajo is not None:
            if nuevo.month < nodoB.abajo.month:
                bandera = 1
                break
            if nodoB.abajo is not None:
                nodoB = nodoB.abajo
        if bandera == 1:
            nodoB.abajo.arriba = nuevo
            nuevo.abajo = nodoB.abajo
            nodoB.abajo = nuevo
            nuevo.arriba = nodoB
        if bandera == 0:
            nodoB.abajo = nuevo
            nuevo.arriba = nodoB
        
        retorno = nuevo
        return retorno
    
    #cuando fila y columna existen usare e metodo que coloca el dato en la pos correcta
    def coloca_d_fila_posicion_correcta(self, nodoB, year, nuevo):
        bandera = 0
        retorno = None
        while nodoB.siguiente is not None:
            if self.devuelve_indice_year(year) < self.devuelve_indice_year(nodoB.siguiente.year):
                bandera = 1
                break
            if self.devuelve_indice_year(year) == self.devuelve_indice_year(nodoB.siguiente.year):
                bandera = 2
                break
            if nodoB.siguiente is not None:
                nodoB = nodoB.siguiente
            else:
                break
        if bandera == 1:
            nodoB.siguiente.anterior = nuevo
            nuevo.siguiente = nodoB.siguiente
            nodoB.siguiente = nuevo
            nuevo.anterior = nodoB
            retorno = nuevo
        if bandera == 0:
            nodoB.siguiente = nuevo
            nuevo.anterior = nodoB
            retorno = nuevo
        if bandera == 2:
            retorno = None
            self.coloca_3D_de_Cubo(nodoB.siguiente, nuevo)
        return retorno
    
    # coloca el nodo en 3D
    def coloca_3D_de_Cubo(self, nodoB, nuevo):
        while True:
            if nodoB.adelante is None:
                print("En 3D")
                break
            nodoB = nodoB.adelante
        nodoB.adelante = nuevo
        nuevo.atras = nodoB
        return nuevo
    
    #colocolar en columna con posición correcta
    def coloca_d_colum_posicion_correcta(self, nodoB, nuevo):
        bandera = 0
        retorno = None
        while nodoB.abajo is not None:
            if nuevo.month < nodoB.abajo.month:
                bandera = 1
                break
            if nodoB.abajo is not None:
                nodoB = nodoB.abajo
        if bandera == 1:
            nodoB.abajo.arriba = nuevo
            nuevo.abajo = nodoB.abajo
            nodoB.abajo = nuevo
            nuevo.arriba = nodoB
        if bandera == 0:
            nodoB.abajo = nuevo
            nuevo.arriba = nodoB
        retorno = nuevo
        return retorno
    
    #busca un nodo existente y me lo devuelve para insertar un nuevo evento
    def buscar_nodo(self, year, month, day):
        cabecera_fila = self.encuentra_fila(month)
        retorno = None
        while cabecera_fila is not None:
            if cabecera_fila.day == day and cabecera_fila.month == month and cabecera_fila.year == year:
                retorno = cabecera_fila
                break
            if cabecera_fila.adelante is not None:
                retorno = self.buscar_3D(cabecera_fila, day, month, year)
                if retorno is not None:
                    break
            if cabecera_fila.siguiente is not None:
                cabecera_fila = cabecera_fila.siguiente
            else:
                break
        return retorno
    
    def buscar_3D(self, nodoB, day, month, year):
        aux = nodoB
        aux = nodoB.adelante
        retorno = None
        while aux is not None:
            if aux.day == day and aux.month == month and aux.year == year:
                retorno = aux
                break
            if aux.adelante is not None:
                aux = aux.adelante
            else:
                break
        return retorno

    def texto_matriz3D(self, nodoB):
        print("entro cadena3d")
        aux1 = nodoB.adelante
        retorno = ""
        while aux1 is not None:
            if aux1.day is not None:
                if aux1.adelante is not None:
                    retorno = retorno +'"'+ str(aux1.day+"/"+aux1.month+"/"+aux1.year)+'"->"'+str(aux1.adelante.day+"/"+aux1.adelante.month+"/"+aux1.adelante.year)+'";\n'
                else:
                    retorno = retorno +'"'+str(aux1.day+"/"+aux1.month+"/"+aux1.year)+'";\n'
                if aux1.atras is not None:
                    retorno = retorno + '"'+ str(aux1.day+"/"+aux1.month+"/"+aux1.year)+'"->"'+str(aux1.atras.day+"/"+aux1.atras.month+"/"+aux1.atras.year)+'";\n'
                else:
                    retorno = retorno +'"'+str(aux1.day+"/"+aux1.month+"/"+aux1.year)+'";\n'
                aux1 = aux1.adelante
        return retorno 
    
    
    def alinear_niveles(self):
        auxfila = self.raiz
        cadena = ""
        while auxfila is not None:
            aux2 = auxfila
            cadena = cadena + "{rank=same "
            while aux2 is not None:
                cadena = cadena +'"'+str(aux2.day+"/"+aux2.month+"/"+aux2.year)+'"; '
                if aux2.siguiente is not None:
                    aux2 = aux2.siguiente
                else:
                    break
            cadena = cadena+"}\n"
            if auxfila.abajo is not None:
                auxfila = auxfila.abajo
            else:
                break
        return cadena

    def cadena_DOT(self):
        auxfil = self.raiz
        retorno = "digraph Matriz{\n"
        retorno = retorno + "node [shape=box, color=cornflowerblue ];\n"
        retorno = retorno + self.alinear_niveles()
        while auxfil is not None:
            aux2 = auxfil
            while aux2 is not None:
                if aux2.adelante is not None:
                    retorno = retorno +'"'+str(aux2.day+"/"+aux2.month+"/"+aux2.year)+'"->'+ self.texto_matriz3D(aux2)
                if aux2.abajo is not None:
                    retorno = retorno +'"'+ str(aux2.day+"/"+aux2.month+"/"+aux2.year)+'"->"'+str(aux2.abajo.day+"/"+aux2.abajo.month+"/"+aux2.abajo.year)+'";\n'
                else:
                    retorno = retorno +'"'+ str(aux2.day+"/"+aux2.month+"/"+aux2.year)+'";\n'
                if aux2.arriba is not None:
                    retorno = retorno +'"'+ str(aux2.day+"/"+aux2.month+"/"+aux2.year)+'"->"'+str(aux2.arriba.day+"/"+aux2.arriba.month+"/"+aux2.arriba.year)+'";\n'
                else:
                    retorno = retorno +'"'+str(aux2.day+"/"+aux2.month+"/"+aux2.year)+'";\n'
                if aux2.siguiente is not None:
                    retorno = retorno + '"'+ str(aux2.day+"/"+aux2.month+"/"+aux2.year)+'"->"'+str(aux2.siguiente.day+"/"+aux2.siguiente.month+"/"+aux2.siguiente.year)+'";\n'
                else:
                    retorno = retorno +'"'+str(aux2.day+"/"+aux2.month+"/"+aux2.year)+'";\n'
                if aux2.anterior is not None:
                    retorno = retorno + '"'+ str(aux2.day+"/"+aux2.month+"/"+aux2.year)+'"->"'+str(aux2.anterior.day+"/"+aux2.anterior.month+"/"+aux2.anterior.year)+'";\n'
                else:
                    retorno = retorno +'"'+str(aux2.day+"/"+aux2.month+"/"+aux2.year)+'";\n'
                aux2 = aux2.siguiente
            auxfil = auxfil.abajo
        retorno = retorno + "}"
        return retorno

    #ver los años registrados
    def print_years(self):
        aux = self.raiz.siguiente
        while aux is not None:
            print("| "+ str(aux.year)+" |")
            aux = aux.siguiente
    
    def print_months(self):
        aux = self.raiz.abajo
        while aux is not None:
            print("| "+str(aux.month)+" |")
            aux = aux.abajo
    
    def move_abajo(self):
        if self.node.abajo is not None:
            self.node = self.node.abajo
            print("| "+str(self.node.day)+"/"+str(self.node.month)+"/"+str(self.node.year)+" |")
    
    def move_arriba(self):
        if self.node.arriba is not None:
            self.node = self.node.arriba
            print("| "+str(self.node.day)+"/"+str(self.node.month)+"/"+str(self.node.year)+" |")
    
    def move_siguiente(self):
        if self.node.siguiente is not None:
            self.node = self.node.siguiente
            print("| "+str(self.node.day)+"/"+str(self.node.month)+"/"+str(self.node.year)+" |")
    
    def move_anterior(self):
        if self.node.anterior is not None:
            self.node = self.node.anterior
            print("| "+str(self.node.day)+"/"+str(self.node.month)+"/"+str(self.node.year)+" |")
    
    def move_adelante(self):
        if self.node.adelante is not None:
            self.node = self.node.adelante
            print("| "+str(self.node.day)+"/"+str(self.node.month)+"/"+str(self.node.year)+" |")
    
    def move_atras(self):
        if self.node.atras is not None:
            self.node = self.node.atras
            print("| "+str(self.node.day)+"/"+str(self.node.month)+"/"+str(self.node.year)+" |")
    
    def devuelve_indice_year(self, year):
        index = 0
        nodoB = self.raiz
        while nodoB.siguiente is not None:
            if nodoB.siguiente.year == year:
                break
            index = index+1
            nodoB = nodoB.siguiente
        return index
