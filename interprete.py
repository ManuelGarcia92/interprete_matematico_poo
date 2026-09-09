from nodos import ExepcionReturn

class Interprete:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones

    def evaluar(self, memoria):
        resultado = None
        if self.instrucciones is not None:
            try:
                for instruccion in self.instrucciones:
                    resultado = instruccion.evaluar(memoria)
            except ExepcionReturn as ret:
                    return ret
            return resultado
        return None


