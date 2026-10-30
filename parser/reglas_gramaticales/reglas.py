from .acciones import AccionesGramaticales

class ReglasGramaticales:
    def __init__(self, flujo):
        self.flujo = flujo
        self.acciones = AccionesGramaticales(self.flujo)

    def parsear_instrucciones(self):
        instruccion = None

        if self.flujo.coincide("VAR"):
            instruccion = self.acciones.parsear_variables(self._expresion)
            
        elif self.flujo.coincide("DEF"):
            instruccion = self.acciones.parsear_funcion(self._expresion, self.parsear_instrucciones)
            
        else:
            instruccion = self._expresion()
            
        return instruccion
        
    def _expresion(self):
        return self.acciones.parsear_binario_izquierdo(self._termino, "SUMA", "RESTA")

    def _termino(self):
        return self.acciones.parsear_binario_izquierdo(self._potencia, "MULTI", "DIV", "DIV_ENTERA", "MOD")
    
    def _potencia(self):
        return self.acciones.parsear_binario_derecho(self._factor, "POTENCIA", "RAIZ_ENESIMA")

    def _factor(self):
        if self.flujo.coincide("NUMERO"):
            return self.acciones.parsear_numeros()
        
        if self.flujo.coincide("IDENTIFICADOR"):
            return self.acciones.parsear_llamada(self._expresion)
        
        if self.flujo.coincide("SUMA", "RESTA"):
            return self.acciones.parsear_unario(self._potencia)
        
        if self.flujo.coincide("PAREN_IZQ"):
            return self.acciones.parsear_parentesis(self._expresion)

        self.flujo.levantar_error("Se esperaba un factor, expresión o identificador")