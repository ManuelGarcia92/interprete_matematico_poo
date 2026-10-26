from nodos import NodoAsignacion, NodoFuncion, NodoLlamadaFun, NodoLlamadaVar, NodoUnario

class AccionesGramaticales:
    def __init__(self, flujo):
        self.flujo = flujo

    def parsear_asignacion(self, metodo_expresion):
        token_identificador = self.flujo.consumir("IDENTIFICADOR", "Falta el nombre de la variable")
        self.flujo.consumir("IGUAL", "Falta el signo de asignación = ")
        expresion = metodo_expresion()
        return NodoAsignacion(token_identificador.valor, expresion)

    def parsear_funcion(self, metodo_argumentos, metodo_cuerpo):
        self.flujo.avanzar()
        token_identificador = self.consumir("IDENTIFICADOR", "Se esperaba el nombre de la función")
        argumentos = self._parsear_argumentos(metodo_argumentos)
        cuerpo = self._parsear_cuerpo(metodo_cuerpo)
        return NodoFuncion(token_identificador.valor, argumentos, cuerpo)

    def parsear_llamada(self, metodo_expresion):
        token_llamada = self.flujo.avanzar()
        if self.flujo.coincide("PAREN_IZQ"):
            argumentos = self._parsear_argumentos(metodo_expresion)
            return NodoLlamadaFun(token_llamada.valor, argumentos)
        return NodoLlamadaVar(token_llamada.valor)
    
    def parsear_parentesis(self, metodo_expresion):
        self.flujo.avanzar()
        expresion = metodo_expresion()
        self.flujo.consumir("PAREN_DER", "No cerraste un paréntesis")
        return expresion
    
    def parsear_unario(self, metodo_potencia):
        token_signo = self.flujo.avanzar()
        if self.flujo.coincide("SUMA", "RESTA"):
            self.flujo.levantar_error("Operador repetido")
        return NodoUnario(token_signo.valor, metodo_potencia())
    
    def parsear_secuencia(self, metodo):
        instruccion = [metodo()]
        while self.flujo.coincide("COMA"):
            self.flujo.avanzar()
            instruccion.append(metodo())
        return instruccion

    def _parsear_argumentos(self, metodo):
        argumentos = []
        self.flujo.consumir("PAREN_IZQ", "Falta el paréntesis de apertura ( en los argumentos")
        if not self.flujo.coincide("PAREN_DER"):
            argumentos = self.parsear_secuencia(metodo)
        self.flujo.consumir("PAREN_DER", "Falta el paréntesis de cierre ) en los argumentos")
        return argumentos
    
    def _parsear_cuerpo(self, metodo_cuerpo):
        self.consumir("LLAVE_IZQ", "El cuerpo de una función debe estar definido dentro de llaves { }")
        if not self.flujo.coincide("LLAVE_DER"):
            cuerpo = metodo_cuerpo()
        self.flujo.consumir("LLAVE_DER", "Falta la llave de cierre } del cuerpo")
        return cuerpo
    
      

    