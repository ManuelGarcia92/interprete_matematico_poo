class TablaDeSimbolos:
    def __init__(self, padre=None):
        self.memoria = {}
        self.padre = padre

    def crear_entorno_local(self):
        return TablaDeSimbolos(padre=self)
    
    def declarar_variable(self, nombre, valor):
        self.memoria[nombre] = valor

    def declarar_funcion(self, nombre, argumentos, cuerpo, entorno):
        if nombre in self.memoria:
            raise Exception(f"La función {nombre} ya ha sido declarada")
        self.memoria[nombre] = {"argumentos": argumentos, "cuerpo": cuerpo, "entorno" : entorno}

    def obtener_simbolo(self, nombre):
        if nombre in self.memoria:
            return self.memoria[nombre]
        elif self.padre is not None:
            return self.padre.obtener_simbolo(nombre)
        raise Exception(f"{nombre} no esta definida")
      
