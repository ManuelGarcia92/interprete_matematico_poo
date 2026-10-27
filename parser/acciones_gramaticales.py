from arbol import nodos

class AccionesGramaticales:
    def __init__(self, flujo):
        self.flujo = flujo

    def parsear_variable(self, metodo_expresion):
        instruccion = self.parsear_secuencia(lambda:self.parsear_asignacion(metodo_expresion))
        self.flujo.consumir("PUNTO_Y_COMA", "La secuencia debe finalizar con ; ")
        return instruccion
    
    def parsear_asignacion(self, metodo_expresion):
        token_nombre_variable = self.flujo.consumir("IDENTIFICADOR", "Falta el nombre de la variable")
        self.flujo.consumir("IGUAL", "Falta el signo de asignación = ")
        expresion = metodo_expresion()
        return nodos.NodoDeclaracionVariable(token_nombre_variable.valor, expresion)
    
    def parsear_funcion(self, metodo_argumentos, metodo_cuerpo):
        token_nombre_funcion = self.flujo.consumir("IDENTIFICADOR", "Se esperaba el nombre de la función")
        argumentos = self._parsear_argumentos(metodo_argumentos)
        cuerpo = self._parsear_cuerpo(metodo_cuerpo)
        return nodos.NodoDeclaracionFuncion(token_nombre_funcion.valor, argumentos, cuerpo)

    def parsear_llamada(self, metodo_expresion):
        token_llamada = self.flujo.avanzar()
        if self.flujo.coincide("PAREN_IZQ"):
            argumentos = self._parsear_argumentos(metodo_expresion)
            return nodos.NodoLlamadaFuncion(token_llamada.valor, argumentos)
        return nodos.NodoLlamadaVariable(token_llamada.valor)
    
    def parsear_parentesis(self, metodo_expresion):
        self.flujo.avanzar()
        expresion = metodo_expresion()
        self.flujo.consumir("PAREN_DER", "No cerraste un paréntesis")
        return expresion
    
    def parsear_unario(self, metodo_potencia):
        token_signo = self.flujo.avanzar()
        if self.flujo.coincide("SUMA", "RESTA"):
            self.flujo.levantar_error("Operador repetido")
        return nodos.NodoUnario(token_signo.valor, metodo_potencia())
    
    def parsear_secuencia(self, metodo):
        instruccion = [metodo()]
        while self.flujo.coincide("COMA"):
            self.flujo.avanzar()
            instruccion.append(metodo())
        return instruccion

    def _parsear_argumentos(self, metodo_argumentos):
        argumentos = []
        self.flujo.consumir("PAREN_IZQ", "Falta el paréntesis de apertura ( en los argumentos")
        if not self.flujo.coincide("PAREN_DER"):
            argumentos = self.parsear_secuencia(metodo_argumentos)
        self.flujo.consumir("PAREN_DER", "Falta el paréntesis de cierre ) en los argumentos")
        return argumentos
    
    def _parsear_cuerpo(self, metodo_cuerpo):
        cuerpo = []
        self.flujo.consumir("LLAVE_IZQ", "El cuerpo de una función debe estar definido dentro de llaves { }")
        if not self.flujo.coincide("LLAVE_DER"):
            while not self.flujo.coincide("LLAVE_DER", "FIN"):
                cuerpo.append(metodo_cuerpo())
                if self.flujo.coincide("PUNTO_Y_COMA"):
                    self.flujo.avanzar()
        self.flujo.consumir("LLAVE_DER", "Falta la llave de cierre } del cuerpo")
        return cuerpo
    
      

    