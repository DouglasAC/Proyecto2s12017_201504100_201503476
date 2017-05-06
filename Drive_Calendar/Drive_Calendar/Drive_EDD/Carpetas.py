from Drive_Calendar.Drive_EDD import Archivos
class Nodo_Carpeta:

    def __init__(self, clave):
        self.clave = clave
        self.nombre = "/"+clave
        self.files = Archivos.AVLTree()
        self.sub_carp = ArbolB()

class Pagina:

    def __init__(self,id):
        self.ramas = [Pagina]*5
        self.claves  = [Nodo_Carpeta]*4
        self.cuentas = 0
        self.claves[0] = id
    
    #imprime las claves del nodo (nombre de carpetas)
    def print_node(self):
        cadena = ""
        for x in range(0, self.cuentas):
            cadena = cadena + "| "+str(self.claves[x].clave)+" |"
        return cadena

class ArbolB:

    def __init__(self):
        self.p = Pagina(None)
        self.right = Pagina(None)
        self.left = Pagina(None)
        self.aux = None
        self.auxr = None
        self.Existe = False
        self.Band1 = False
        self.cadena = ""
        self.lista_aux = list()
        self.lista_cad = list()
    
    def is_empty(self, pagina):
        if pagina is None or pagina.cuentas is 0:
            return True
        else:
            return False
    
    def insertar(self, cla):
        cl = Nodo_Carpeta(cla)
        self.insertar_p(cl, self.p)
    
    def insertar_p(self, cl, raiz):
        print("insertar: "+str(cl.clave))
        self.empujar(cl, raiz)
        if(self.Band1==True):
            print("nueva")
            self.p = Pagina(None)
            self.p.cuentas = 1
            self.p.claves[0] = self.aux
            self.p.ramas[0] = raiz
            self.p.ramas[1] = self.auxr
    
    def empujar(self, cl, raiz):
        print("empujar")
        k = 0
        self.Existe = False
        if self.is_empty(raiz) == True:
            self.Band1 = True
            self.aux = cl
            self.auxr = None
        else:
            k = self.buscar_nodo(cl, raiz)
            if self.Existe == True:
                print("Clave Repetida")
                self.Band1 = False
            else:
                self.empujar(cl, raiz.ramas[k])
                if(self.Band1==True):
                    if raiz.cuentas < 4:
                        self.Band1 = False
                        self.meter_pagina(self.aux, raiz, k)
                    else:
                        self.Band1 = True
                        self.dividr_Nodo(self.aux, raiz, k)
    
    def meter_pagina(self, cl, raiz, k):
        x = raiz.cuentas
        while x is not k:
            raiz.claves[x] = raiz.claves[x-1]
            raiz.ramas[x+1] = raiz.ramas[x]
            x = x-1
        raiz.claves[k] = cl
        raiz.ramas[k+1] = self.auxr
        raiz.cuentas = raiz.cuentas+1
    
    def dividr_Nodo(self, clave, raiz, k):
        posi = 0
        posmda = 0
        if k <= 2:
            posmda = 2
        else:
            posmda = 3
        pagina_der = Pagina(None)
        pos = posmda + 1
        while pos is not 5:
            pagina_der.claves[(pos-posmda)-1] = raiz.claves[pos-1]
            pagina_der.ramas[pos-posmda] = raiz.ramas[pos]
            pos = pos+1
        pagina_der.cuentas = 4 - posmda
        raiz.cuentas = posmda
        if k <= 2:
            self.meter_pagina(clave, raiz, k)
        else:
            self.meter_pagina(clave, pagina_der, (k-posmda))
        self.aux = raiz.claves[raiz.cuentas - 1]
        pagina_der.ramas[0] = raiz.ramas[raiz.cuentas]
        raiz.cuentas = raiz.cuentas - 1
        self.auxr = pagina_der
    
    def buscar_nodo(self, cl, raiz):
        x = 0
        if cl.clave < raiz.claves[0].clave:
            self.Existe = False
            x = 0
        else:
            x = raiz.cuentas
            while cl.clave < raiz.claves[x-1].clave and x > 1:
                x = x - 1
            if cl.clave == raiz.claves[x - 1].clave:
                self.Existe = True
            else:
                self.Existe = False
        return x
    
    def imprimir_arbol(self):
        self.cadena = ""
        self.enlazar_ramas(self.p)
        return self.cadena
    
    def enlazar_ramas(self, pagina):
        if(pagina.cuentas > 0) and (pagina.ramas[0] is not None):
            for x in range(0, pagina.cuentas + 1):
                if pagina.ramas[x] is not None:
                    if pagina.ramas[x].print_node() is not "":
                        self.cadena = self.cadena + '"'+pagina.print_node() +'"'+' -> "'+ pagina.ramas[x].print_node()+'";'+"\n"
                    if pagina.ramas[x].print_node() is "":
                        self.cadena = self.cadena + '"'+pagina.print_node() +'";\n'
                    self.enlazar_ramas(pagina.ramas[x])
    
    def eliminar_publico(self, clave):
        self.eliminar(self.p, clave)
        self.lista_aux.remove(clave)
        self.p = Pagina(None)
        self.re_insert()
        
    def eliminar(self, pagina, cl):
        if(pagina.cuentas > 0) and (pagina.ramas[0] is not None):
            for x in range (0, pagina.cuentas+1):
                if pagina.ramas[x] is not None:
                    self.recorre_nodo(pagina)
                    self.recorre_nodo(pagina.ramas[x])
                    self.eliminar(pagina.ramas[x], cl)
    
    def recorre_nodo(self, pagina):
        for x in range(0, pagina.cuentas):
            if pagina.claves[x].clave in self.lista_aux:
                pass
            else:
                self.lista_aux.append(pagina.claves[x])
    
    def re_insert(self):
        for c in self.lista_aux:
            self.insertar(c)
    
    def print_root(self):
        print(self.p.print_node())
    
    def listar_carpetas(self):
        #metodo publico
        self.lista_aux.clear()
        self.listar(self.p)
        return self.lista_aux
        

    def listar(self, pagina):
        if(pagina.cuentas > 0) and (pagina.ramas[0] is not None):
            self.meter_a_lista(pagina)
            for x in range(1, pagina.cuentas+1):
                if pagina.ramas[x] is not None:
                    self.meter_a_lista(pagina.ramas[x])
                    self.listar(pagina.ramas[x-1])
    
    def meter_a_lista(self, pagina):
        for x in range(0, pagina.cuentas):
            self.lista_aux.append(pagina.claves[x])
    
    def listar_string(self):
        self.lista_cad.clear()
        self.listar_cadenas(self.p)
        return self.lista_cad

    def listar_cadenas(self, pagina):
        if(pagina.cuentas > 0) and (pagina.ramas[0] is not None):
            self.meter_cadenas(pagina)
            for x in range(1, pagina.cuentas+1):
                if pagina.ramas[x] is not None:
                    self.meter_cadenas(pagina.ramas[x])
                    self.listar_cadenas(pagina.ramas[x-1])
    
    def meter_cadenas(self, pagina):
        for x in range(0, pagina.cuentas):
            self.lista_aux.append(pagina.claves[x].clave)
        
