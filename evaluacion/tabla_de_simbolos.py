class TablaDeSimbolos:
    def __init__(self, padre=None):
        self.memoria = {}
        self.padre = padre

    def imprimir_memoria(self):
        if self.memoria:
            print(":::::MEMORIA:::::")
            variables = {n: v for n, v in self.memoria.items() if not isinstance(v, dict)}
            funciones = {n: v for n, v in self.memoria.items() if isinstance(v, dict)}
            if variables:
                for nombre, valor in variables.items():
                    print(f"{nombre} = {valor}")
            if funciones:
                for nombre, datos in funciones.items():
                    args = ", ".join(a.nombre for a in datos["argumentos"])
                    print(f"{nombre}({args})")

    def crear_entorno_local(self):
        return TablaDeSimbolos(padre=self)
    
    def declarar_variable(self, nombre, valor):
        self.memoria[nombre] = valor

    def declarar_funcion(self, nombre, argumentos, cuerpo):
        if nombre in self.memoria:
            raise Exception(f"Error semántico: La función {nombre} ya ha sido declarada.")
        self.memoria[nombre] = {"argumentos": argumentos, "cuerpo": cuerpo}

    def llamar_variable(self, nombre):
        if nombre in self.memoria:
            return self.memoria[nombre]
        if self.padre is not None:
            return self.padre.llamar_variable(nombre)
        raise Exception(f"Error semántico: Variable {nombre} no esta definida.")
      
    def llamar_funcion(self, nombre):
        if nombre not in self.memoria:
            raise Exception(f"Error semántico: La función {nombre} no esta declarada.")
        return self.memoria[nombre]

    def eliminar(self, nombre):
        if nombre not in self.memoria:
            raise Exception(f"{nombre} no esta definida")
        del self.memoria[nombre]