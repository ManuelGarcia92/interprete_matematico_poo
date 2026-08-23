class TablaDeSimbolos:
    def __init__(self):
        self.simbolos = {
            "pi" : 3.1415926536,
            "e"  : 2.7182818285
        }

    def declarar(self, nombre, valor):
        if nombre in self.simbolos:
            raise Exception(f"Error semántico: La variable {nombre} ya ha sido declarada.")
        self.simbolos[nombre] = valor

    def obtener(self, nombre):
        if nombre not in self.simbolos:
            raise Exception(f"Error semántico: La variable {nombre} no esta definida.")
        return self.simbolos[nombre]