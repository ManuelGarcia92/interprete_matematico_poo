class FlujoDeTokens:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def levantar_error(self, mensaje):
        raise Exception(mensaje)
    
    def mirar(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
            
    def avanzar(self):
        token_actual = self.mirar()
        if token_actual:
            self.pos += 1
            return token_actual
        return None
            
    def coincide(self, *tipos):
        token_actual = self.mirar()
        if token_actual and token_actual.tipo in tipos:
            return token_actual
        return None
    
    def consumir(self, tipo_esperado, mensaje_error):
        if self.coincide(tipo_esperado):
            return self.avanzar()
        self.levantar_error(mensaje_error)   

    def levantar_error(self, mensaje):
        raise Exception(f"ERROR [Linea : {self.mirar().linea} Columna: {self.mirar().columna} Token : {self.mirar().valor} : {mensaje}]\n")
    
    
    
        
    
    
            