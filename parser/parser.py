from .flujo_de_tokens import FlujoDeTokens
from .reglas_gramaticales import ReglasGramaticales

class Parser:
    def __init__(self, tokens : list):
        self.flujo = FlujoDeTokens(tokens)
        self.reglas = ReglasGramaticales(self.flujo)

    def parsear(self) -> list:
        instrucciones = []

        if self.flujo.coincide("FIN"):
            instrucciones = None

        while not self.flujo.coincide("FIN"):
            instrucciones.append(self.reglas.parsear_instrucciones())
            
        self.flujo.consumir("FIN", "Quedan tokens sin procesar")

        return instrucciones