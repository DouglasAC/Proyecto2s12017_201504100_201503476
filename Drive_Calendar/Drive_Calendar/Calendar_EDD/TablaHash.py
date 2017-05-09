from Drive_Calendar.Calendar_EDD import NodoEvento
#import NodoEvento
class TablaHash:

	def funcionMain(self):
		pass
		#self.insertar("evento1","direccion","fecha","descripcion1","hora1")
		#self.insertar("hola1","holadic","hola","hola2","hola2")
		#print ("mostrar Tabla")
		#self.mostrarTabla()
	def __init__(self):
	
		self.tabla = [NodoEvento.Nodo()]*120
	def insertar(self,nombre,direccion,fecha,descripcion,hora):
		nuevoEvento = NodoEvento.Nodo()
		nuevoEvento.nombre = nombre
		nuevoEvento.direccion = direccion
		nuevoEvento.fecha = fecha
		nuevoEvento.descripcion = descripcion
		nuevoEvento.hora = hora
		clave_evento = self.codificar(nuevoEvento.nombre)
		indice = self.funcionHash(clave_evento)
		colision = self.hayColision(indice)
		if colision == False:
			self.tabla[int(indice)] = nuevoEvento
			
		else:
			self.recuperacionLineal(nuevoEvento,indice)
		
		
		
	def codificar(self,mensaje):
		codificar = list(mensaje)
		clave = ""
		for i  in range(len(codificar)):
			clave = clave + str(ord(codificar[i]))
		return clave	
		
	def funcionHash(self,clave):
		funcion = int(clave) ** 2
		f = list(str(funcion))
		indice = str(f[int(len(f)/2)]) + str(f[int(len(f)/2+1)])
		return indice
	
	def hayColision(self,indice):
		retornar = False
		
		if self.tabla[int(indice)].nombre != "":
			retornar = True
		return retornar
		
	def recuperacionLineal(self,evento,indice):
		i=int(indice)
		noinserto = True
		while(noinserto):
			for i in range(len(self.tabla)):
				if self.tabla[i].nombre == "":
					self.tabla[i] = evento
					noinserto= False

			i=0
		
	def mostrarTabla(self):
		i=0
		print ("mostrar Tabla****")
		for i in range(len(self.tabla)):
			if self.tabla[i].nombre == "":
				print (" No hay evento ",str(i))
			else:
				print ("Encontro dato en la posicion" + str(i))
				#print (str(self.tabla[i].nombre) + "posicion " + str(indice))
	
	def buscarDato(self,nombre):
		retornar = None
		clave = self.codificar(nombre)
		indice = self.funcionHash(clave)
		haycolision = self.hayColision(indice)
		noencontro= True
		if haycolision==True:
			i = int(indice) + 1
			while(noencontro):
				if self.tabla[i].nombre == nombre:
					retornar = self.tabla[i]
					noencontro = False
				else:
					i = i+1
		else:
			retornar = self.tabla[i]
		return retornar
	
	def eliminar(self,nombre):	
		clave = self.codificar(nombre)
		indice = self.funcionHash(clave)
		haycolision = self.hayColision(indice)
		noencontro= True
		if haycolision==True:
			i = int(indice) + 1
			while(noencontro):
				if self.tabla[i].nombre == nombre:
					self.tabla[i].nombre = ""
					self.tabla[i].direccion = ""
					self.tabla[i].fecha = ""
					self.tabla[i].descripcion = ""
					self.tabla[i].hora = ""
					
					noencontro = False
				else:
					i = i+1
		else:
				self.tabla[i].nombre = ""
				self.tabla[i].direccion = ""
				self.tabla[i].fecha = ""
				self.tabla[i].descripcion = ""
				self.tabla[i].hora = ""
		
	def reporteHash(self):
		estilos = " <style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}td, th {    border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style>"
		cadenahtml = "<html>\n<head>"+estilos+"</head>\n"
		cadenahtml = cadenahtml + "<body>\n"
		cadenahtml = cadenahtml + "<table>\n"
		cadenahtml = cadenahtml + "<tr>\n<th>Indice</th><th>Nombre</th><th>fecha</th></tr>"
		for i in range(len(self.tabla)):
    		#if self.tabla.nombre is not "":
    		#cadenahtml = cadenahtml + "<tr>\n"
			#adenahtml = cadenahtml + "<td>"+str(i)+"</td>"
		#cadenahtml = cadenahtml + "</br>"
		#cadenahtml = cadenahtml + "</table>/</body></html>"
		#return cadenahtml
		
		
		
		
		
		
		
		
			
		
	
		