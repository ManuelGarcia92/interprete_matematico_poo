class Interprete:
    def __init__(self, arboles):
        self.arboles = arboles

    def evaluar(self, memoria):
        resultado = None
        for arbol in self.arboles:
            resultado = arbol.evaluar(memoria)
        return resultado
        

