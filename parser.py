from nodos import NodoBinario, NodoPotencia, NodoNumero
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.puntero = 0

    def advance(self):
        token = self.tokens[self.puntero]
        self.puntero += 1
        return token
    
    def peek(self):
        if self.tokens[self.puntero].tipo == "FIN":
            return None
        return self.tokens[self.puntero]
    
    def match(self, tipo):
        token = self.peek()
        return token is not None and token.tipo == tipo
    
    def expr(self):
        nodo = self.term()
        while self.match("SUMA") or self.match("RESTA"):
            operador = self.advance()
            derecha = self.term()
            nodo = NodoBinario(nodo, operador.valor, derecha)
        return nodo
    
    def term(self):
        nodo = self.potencia()
        while self.match("MULTIPLICACION") or self.match("DIVISION") or self.match("DIVI_ENTERA"):
            operador = self.advance()
            derecha = self.potencia()
            nodo = NodoBinario(nodo, operador.valor, derecha)
        return nodo   
    
    def potencia(self):
        base = self.factor()
        if self.match("POTENCIA"):
            self.advance()
            exponente = self.potencia()
            return NodoPotencia(base, exponente)
        return base 

    def factor(self):
        if self.match("PAREN_IZQ"):
            self.advance()
            paren_tree = self.expr()
            if self.peek().tipo != "PAREN_DER":
                raise Exception("No cerraste un parentesis")
            self.advance()
            return paren_tree
        elif self.match("NUMERO"):
            token = self.advance()
            return NodoNumero(token.valor)
        else:
            raise Exception("Esperaba un número")
            
    
    

  

