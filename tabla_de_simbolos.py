class TablaDeSimbolos:
    def __init__(self, padre = None):
        self.padre = padre
        self.simbolos = {}
        self.funciones = {}

        if self.padre is None:
            self.simbolos["pi"] = 3.1415926536
            self.simbolos["e"]  = 2.7182818285
                 
    def declarar(self, nombre, valor):
        self.simbolos[nombre] = valor

    def obtener(self, nombre):
        if nombre in self.simbolos:
            return self.simbolos[nombre]
        if self.padre is not None:
            return self.padre.obtener(nombre)
        raise Exception(f"Error semántico: Variable {nombre} no esta definida.")
      
    def crear_entorno_local(self):
        return TablaDeSimbolos(padre=self)

    def declarar_funcion(self, nombre, argumentos, codigo):
        if nombre in self.funciones:
            raise Exception(f"Error semántico: La función {nombre} ya ha sido declarada.")
        self.funciones[nombre] = {"argumentos": argumentos, "codigo": codigo}

    def llamar_funcion(self, nombre):
        if nombre not in self.funciones:
            raise Exception(f"Error semántico: La función {nombre} no esta declarada.")
        return self.funciones[nombre]