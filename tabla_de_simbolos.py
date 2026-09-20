class TablaDeSimbolos:
    def __init__(self, padre=None):
        self.memoria = {}
        self.padre = padre
                
    def declarar(self, nombre, valor):
        self.memoria[nombre] = valor

    def obtener(self, nombre):
        if nombre in self.memoria:
            return self.memoria[nombre]
        if self.padre is not None:
            return self.padre.obtener(nombre)
        raise Exception(f"Error semántico: Variable {nombre} no esta definida.")
      
    def crear_entorno_local(self):
        return TablaDeSimbolos(padre=self)

    def declarar_funcion(self, nombre, argumentos, cuerpo):
        if nombre in self.memoria:
            raise Exception(f"Error semántico: La función {nombre} ya ha sido declarada.")
        self.memoria[nombre] = {"argumentos": argumentos, "cuerpo": cuerpo}

    def llamar_funcion(self, nombre):
        if nombre not in self.memoria:
            raise Exception(f"Error semántico: La función {nombre} no esta declarada.")
        return self.memoria[nombre]