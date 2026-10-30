class EstructurasGramaticales:
    def __init__(self, flujo):
        self.flujo = flujo

    def parsear_argumentos(self, metodo_argumentos):
        argumentos = []
        self.flujo.consumir("PAREN_IZQ", "Falta el paréntesis de apertura ( en los argumentos")
        if not self.flujo.coincide("PAREN_DER"):
            argumentos = self.parsear_secuencia(metodo_argumentos)
        self.flujo.consumir("PAREN_DER", "Falta el paréntesis de cierre ) en los argumentos")
        return argumentos
    
    def parsear_cuerpo(self, metodo_cuerpo):
        cuerpo = []
        self.flujo.consumir("LLAVE_IZQ", "El cuerpo de una función debe estar definido dentro de llaves { }")
        while not self.flujo.coincide("LLAVE_DER", "FIN"):
            cuerpo.append(metodo_cuerpo())
        self.flujo.consumir("LLAVE_DER", "Falta la llave de cierre } del cuerpo")
        return cuerpo

    def parsear_secuencia(self, metodo):
        secuencia = [metodo()]
        while self.flujo.coincide("COMA"):
            self.flujo.avanzar()
            secuencia.append(metodo())
        return secuencia