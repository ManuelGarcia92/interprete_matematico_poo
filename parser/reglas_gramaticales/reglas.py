from .acciones import AccionesGramaticales

class ReglasGramaticales:
    def __init__(self, flujo):
        self.flujo = flujo
        self.acciones = AccionesGramaticales(self.flujo)

    def parsear_instrucciones(self):
        if self.flujo.coincide("PRINT"):
            return self.acciones.parsear_salida(self._expresion)
        
        if self.flujo.coincide("VAR"):
            return self.acciones.parsear_variables(self._expresion)
            
        if self.flujo.coincide("DEF"):
           return self.acciones.parsear_funcion(self._expresion, self.parsear_instrucciones)
            
        return self._expresion()
            
    def _expresion(self):
        return self.acciones.parsear_binario_izquierdo(self._termino, "OP_EXPRE")

    def _termino(self):
        return self.acciones.parsear_binario_izquierdo(self._potencia, "OP_TERM")
    
    def _potencia(self):
        return self.acciones.parsear_binario_derecho(self._factor, "OP_POTEN")

    def _factor(self):
        if self.flujo.coincide("NUMERO"):
            return self.acciones.parsear_numeros()
        
        if self.flujo.coincide("IDENTIFICADOR"):
            return self.acciones.parsear_llamada(self._expresion)
        
        if self.flujo.coincide("OP_EXPRE"):
            return self.acciones.parsear_unario(self._potencia)
        
        if self.flujo.coincide("PAREN_IZQ"):
            return self.acciones.parsear_parentesis(self._expresion)

        self.flujo.levantar_error("Se esperaba un factor, expresión o identificador")