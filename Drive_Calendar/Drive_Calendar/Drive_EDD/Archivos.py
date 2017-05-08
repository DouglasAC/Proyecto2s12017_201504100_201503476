class Archivo:

    def __init__(self, nombre, extension, archivo):
        self.nombre = nombre
        self.extension = extension
        self.archivo = archivo #archivo ya en bytes
        self.size = ""
    
class Node(object):
        
        # la llave es el nombre del archivo
    def __init__(self, Archivo, key):
        self.file = Archivo
        self.left = None
        self.right = None
        self.key = key

class AVLTree(object):
    
    def __init__(self):
        self.node = None
        self.altura = -1
        self.balance = 0
    
    def agregar(self, nombre, extension, archivo):
        file = Archivo(nombre, extension, archivo)
        nuevo = Node(file, nombre)
        if not self.node:
            self.node = nuevo
            self.node.left = AVLTree()
            self.node.right = AVLTree()
        elif nombre < self.node.key:
            self.node.left.agregar(nombre, extension, archivo)
        elif nombre > self.node.key:
            self.node.right.agregar(nombre, extension, archivo)
        self.rebalance()
    
    def rebalance(self):
        self.actualiza_altura(recursive=False)
        self.actualiza_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotacion_izq()
                    self.actualiza_altura()
                    self.actualiza_balances()
                self.rotacion_der()
                self.actualiza_altura()
                self.actualiza_balances()
            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rotacion_der()
                    self.actualiza_altura()
                    self.actualiza_balances()
                self.rotacion_izq()
                self.actualiza_altura()
                self.actualiza_balances()
    
    def actualiza_altura(self, recursive=True):
        if self.node:
            if recursive:
                if self.node.left:
                    self.node.left.actualiza_altura()
                if self.node.right:
                    self.node.right.actualiza_altura()
            self.altura = 1 + max(self.node.left.altura, self.node.right.altura)
        else:
            self.altura = -1
    
    def actualiza_balances(self, recursive=True):
        if self.node:
            if recursive:
                if self.node.left:
                    self.node.left.actualiza_balances()
                if self.node.right:
                    self.node.right.actualiza_balances()
            self.balance = self.node.left.altura - self.node.right.altura
        else:
            self.balance = 0
    
    def rotacion_der(self):
        raiz_nueva = self.node.left.node
        nueva_izq = raiz_nueva.right.node
        raiz_ant = self.node

        self.node = raiz_nueva
        raiz_ant.left.node = nueva_izq
        raiz_nueva.right.node = raiz_ant
    
    def rotacion_izq(self):
        raiz_nueva = self.node.right.node
        nueva_izq = raiz_nueva.left.node
        raiz_ant = self.node

        self.node = raiz_nueva
        raiz_ant.right.node = nueva_izq
        raiz_nueva.left.node = raiz_ant
    
    def eliminar(self, key):
        if self.node != None:
            if self.node.key == key:
                if not self.node.left.node and not self.node.right.node:
                    self.node = None
                elif not self.node.left.node:
                    self.node = self.node.right.node
                elif not self.node.right.node:
                    self.node = self.node.left.node
                else:
                    sucesor = self.node.right.node
                    while sucesor and sucesor.left.node:
                        sucesor = sucesor.left.node
                    if sucesor:
                        self.node.key = sucesor.key
                        self.node.right.eliminar(sucesor.key)
            elif key < self.node.key:
                self.node.left.eliminar(key)
            elif key > self.node.key:
                self.node.right.eliminar(key)
            self.rebalance()

    def graficar(self):
        cadena = "digraph AVL {\n"
        if self.node != None:
            cadena = self.__listar(self.node, cadena)
            cadena += "\n"
            cadena = self.__enlazar(self.node, cadena)
        cadena += "}"
        return cadena
    
    def __listar(self, raiz, cadena):
        if(raiz != None):
            cadena += "nodo" + str(raiz.key) + "[label=\""+str(raiz.file.nombre)+"."+str(raiz.file.extension)+"\"];\n"
            if(raiz.left != None and raiz.right != None):
                cadena = self.__listar(raiz.left.node, cadena)
                cadena = self.__listar(raiz.right.node, cadena)
            elif(raiz.node.left != None):
                cadena = self.__listar(raiz.left.node, cadena)
            elif(raiz.node.right != None):
                cadena = self.__listar(raiz.right.node, cadena)
        return cadena
    
    def __enlazar(self, raiz, cadena):
        if(raiz != None):
            if(raiz.right.node != None):
                cadena += "nodo"+str(raiz.key)+" -> nodo"+str(raiz.right.node.key)+";\n"
                cadena = self.__enlazar(raiz.right.node, cadena)
            if(raiz.left.node != None):
                cadena += "nodo"+str(raiz.key)+" -> nodo"+str(raiz.left.node.key)+";\n"
                cadena = self.__enlazar(raiz.left.node, cadena)
        return cadena