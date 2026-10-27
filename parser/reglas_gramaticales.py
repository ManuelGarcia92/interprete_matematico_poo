from .acciones_gramaticales import AccionesGramaticales
from arbol.nodos import NodoNumero, NodoBinario

class ReglasGramaticales:
    def __init__(self, flujo):
        self.flujo = flujo
        self.acciones = AccionesGramaticales(self.flujo)

    def parsear_instrucciones(self):
        instruccion = None

        if self.flujo.coincide("VAR"):
            self.flujo.avanzar()
            instruccion = self.acciones.parsear_variable(self.expresion)
            
        elif self.flujo.coincide("DEF"):
            self.flujo.avanzar()
            instruccion = self.acciones.parsear_funcion(self.expresion, self.parsear_instrucciones)
            
        else:
            instruccion = self.expresion()
            
        return instruccion
        
    def expresion(self):
        nodo_izquierdo = self._termino()
        while self.flujo.coincide("SUMA", "RESTA"):
            token_operador = self.flujo.avanzar()
            nodo_derecho = self._termino()
            nodo_izquierdo = NodoBinario(token_operador.valor, nodo_izquierdo, nodo_derecho)
        return nodo_izquierdo

    def _termino(self):
        nodo_izquierdo = self._potencia()
        while self.flujo.coincide("MULTI", "DIV", "DIV_ENTERA", "MOD"):
            token_operador = self.flujo.avanzar()
            nodo_derecho = self._potencia()
            nodo_izquierdo = NodoBinario(token_operador.valor, nodo_izquierdo, nodo_derecho)
        return nodo_izquierdo

    def _potencia(self):
        nodo_izquierdo = self._factor()
        if self.flujo.coincide("POTENCIA", "RAIZ_ENESIMA"):
            token_operador = self.flujo.avanzar()
            nodo_derecho = self._potencia()
            nodo_izquierdo = NodoBinario(token_operador.valor, nodo_izquierdo, nodo_derecho)
        return nodo_izquierdo

    def _factor(self):
        if self.flujo.coincide("NUMERO"):
            token_numero = self.flujo.avanzar()
            return NodoNumero(token_numero.valor)
        
        elif self.flujo.coincide("IDENTIFICADOR"):
            return self.acciones.parsear_llamada(self.expresion)
        
        elif self.flujo.coincide("SUMA", "RESTA"):
            return self.acciones.parsear_unario(self._potencia)
        
        elif self.flujo.coincide("PAREN_IZQ"):
            return self.acciones.parsear_parentesis(self.expresion)

        else:
            self.flujo.levantar_error("Se esperaba un factor, expresión o identificador")