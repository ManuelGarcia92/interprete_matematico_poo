from nodos import NodoSuma, NodoResta, NodoMulti, NodoDiv, NodoDivEntera, NodoPotencia, NodoRaizEnesima, NodoNumero, NodoPositivo, NodoNegativo
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.puntero = 0

    def advance(self):
        token = self.tokens[self.puntero]
        self.puntero += 1
        return token
    
    def peek(self, pasos=0):
        if self.tokens[self.puntero + pasos].tipo == "FIN":
            return None
        return self.tokens[self.puntero + pasos]
    
    def match(self, tipo):
        token = self.peek()
        return token is not None and token.tipo == tipo
    
    def expr(self):
        nodo = self.term()
        while self.match("SUMA") or self.match("RESTA"):
            operador = self.advance()
            derecha = self.term()
            if operador.tipo == "SUMA":
                nodo = NodoSuma(nodo, derecha)
            elif operador.tipo == "RESTA":
                nodo = NodoResta(nodo, derecha)
        return nodo
    
    def term(self):
        nodo = self.raiz_y_potencia()
        while self.match("MULTI") or self.match("DIV") or self.match("DIV_ENTERA"):
            operador = self.advance()
            derecha = self.raiz_y_potencia()
            if operador.tipo == "MULTI":
                nodo = NodoMulti(nodo, derecha)
            elif operador.tipo == "DIV":
                nodo = NodoDiv(nodo, derecha)
            elif operador.tipo == "DIV_ENTERA":
                nodo = NodoDivEntera(nodo, derecha)
        return nodo   
    
    def raiz_y_potencia(self):
        base = self.factor()
        if self.match("POTENCIA"):
            self.advance()
            derecha = self.raiz_y_potencia()
            return NodoPotencia(base, derecha)
        while self.match("RAIZ_ENESIMA"):
            self.advance()
            derecha = self.factor()
            return NodoRaizEnesima(base, derecha)
        return base 

    def factor(self):
        if self.match("PAREN_IZQ"):
            self.advance()
            paren_tree = self.expr()
            if self.peek().tipo != "PAREN_DER":
                raise Exception("No cerraste un parentesis")
            self.advance()
            return paren_tree
        elif self.match("SUMA"):
            self.advance()
            return NodoPositivo(self.factor())
        elif self.match("RESTA"):
            self.advance()
            return NodoNegativo(self.factor())
        elif self.match("NUMERO"):
            token = self.advance()
            return NodoNumero(token.valor)
        else:
            raise Exception("Esperaba un número")
            
    
    

  

