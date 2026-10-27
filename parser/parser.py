from .flujo_de_tokens import FlujoDeTokens
from .reglas_gramaticales import ReglasGramaticales

class Parser:
    def __init__(self, tokens : list):
        self.flujo = FlujoDeTokens(tokens)
        self.reglas = ReglasGramaticales(self.flujo)

    def parsear(self) -> list:
        instrucciones = []
        
        if self.flujo.coincide("FIN"):
            raise Exception("Expresión vacia")

        while not self.flujo.coincide("FIN"):
            instrucciones.append(self.reglas.parsear_instrucciones())

            if self.flujo.coincide("PUNTO_Y_COMA"):
                self.flujo.avanzar()
            
        if self.flujo.mirar() and not self.flujo.coincide("FIN"):
            self.levantar_error("Quedan tokens sin procesar")
        
        return instrucciones