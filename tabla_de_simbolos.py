class TablaDeSimbolos:
    def __init__(self):
        self.simbolos = {
        "pi" : 3.1415926536,
        "e"  : 2.7182818285
    }
        self.funciones = {}

    def declarar(self, nombre, valor):
        if nombre in  ("pi", "e"):
            raise Exception(f"Error semántico: La variable {nombre} ya ha sido declarada.")
        self.simbolos[nombre] = valor

    def obtener(self, nombre):
        if nombre not in self.simbolos:
            raise Exception(f"Error semántico: La variable {nombre} no esta definida.")
        return self.simbolos[nombre]

    def declarar_funcion(self, nombre, argumentos, codigo):
        if nombre in self.funciones:
            raise Exception(f"Error semántico: La función {nombre} ya ha sido declarada.")
        self.funciones[nombre] = {"argumentos": argumentos, "codigo": codigo}

    def llamar_funcion(self, nombre):
        if nombre not in self.funciones:
            raise Exception(f"Error semántico: La función {nombre} no ha sido declarada.")
        return self.funciones[nombre]