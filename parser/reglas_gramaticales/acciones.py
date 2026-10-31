from .estructuras import EstructurasGramaticales
from arbol import nodos

class AccionesGramaticales:
    def __init__(self, flujo):
        self.flujo = flujo
        self.estructuras = EstructurasGramaticales(flujo)

    def parsear_variables(self, metodo_expresion):
        self.flujo.avanzar()
        variables = self.estructuras.parsear_secuencia(lambda:self._parsear_asignacion(metodo_expresion))
        self.flujo.consumir("PUNTO_Y_COMA", "La secuencia debe finalizar con ; ")
        return variables
    
    def _parsear_asignacion(self, metodo_expresion):
        token_nombre_variable = self.flujo.consumir("IDENTIFICADOR", "Falta el nombre de la variable")
        self.flujo.consumir("IGUAL", "Falta el signo de asignación = ")
        expresion = metodo_expresion()
        return nodos.NodoDeclararVariable(token_nombre_variable.valor, expresion)
    
    def parsear_funcion(self, metodo_argumentos, metodo_cuerpo):
        self.flujo.avanzar()
        token_nombre_funcion = self.flujo.consumir("IDENTIFICADOR", "Se esperaba el nombre de la función")
        argumentos = self.estructuras.parsear_argumentos(metodo_argumentos)
        cuerpo = self.estructuras.parsear_cuerpo(metodo_cuerpo)
        return nodos.NodoDeclararFuncion(token_nombre_funcion.valor, argumentos, cuerpo)

    def parsear_binario_izquierdo(self, metodo_inferior, operador):
        nodo_izquierdo = metodo_inferior()
        while self.flujo.coincide(operador):
            token_operador = self.flujo.avanzar()
            nodo_derecho = metodo_inferior()
            nodo_izquierdo = nodos.NodoBinario(token_operador.valor, nodo_izquierdo, nodo_derecho)
        return nodo_izquierdo

    def parsear_binario_derecho(self, metodo_inferior, operador):
        nodo_izquierdo = metodo_inferior()
        if self.flujo.coincide(operador):
            token_operador = self.flujo.avanzar()
            nodo_derecho = self.parsear_binario_derecho(metodo_inferior, operador)
            nodo_izquierdo = nodos.NodoBinario(token_operador.valor, nodo_izquierdo, nodo_derecho)
        return nodo_izquierdo

    def parsear_numeros(self):
        token_numero = self.flujo.avanzar() 
        return nodos.NodoNumero(token_numero.valor)
    
    def parsear_llamada(self, metodo_expresion):
        token_llamada = self.flujo.avanzar()
        if self.flujo.coincide("PAREN_IZQ"):
            argumentos = self.estructuras.parsear_argumentos(metodo_expresion)
            return nodos.NodoLlamarFuncion(token_llamada.valor, argumentos)
        return nodos.NodoLlamarVariable(token_llamada.valor)
    
    def parsear_unario(self, metodo_potencia):
        token_signo = self.flujo.avanzar()
        if self.flujo.coincide("OP_EXPRE"):
            self.flujo.levantar_error("Operador repetido")
        return nodos.NodoUnario(token_signo.valor, metodo_potencia())

    def parsear_parentesis(self, metodo_expresion):
        self.flujo.avanzar()
        expresion = metodo_expresion()
        self.flujo.consumir("PAREN_DER", "No cerraste un paréntesis")
        return expresion
    
    

    