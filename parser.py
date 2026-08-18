from nodos import *
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.puntero = 0

    def advance(self, pasos=0):
        token = self.tokens[self.puntero + pasos]
        self.puntero += 1
        return token
    
    def peek(self, pasos=0):
        return self.tokens[self.puntero + pasos]
    
    def match(self, tipo):
        token = self.peek()
        return token is not None and token.tipo == tipo
    
    def parsear(self):
        if self.match("FIN"):
            raise Exception("Expresión vacia")
        tree = self.expr()

        if self.peek().tipo != "FIN":
            raise Exception(f"ERROR:Quedan tokens sin procesar:\nToken:{self.peek().valor}\nColumna:{self.peek().columna}")
        
        return tree

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

        if self.match("POTENCIA") or self.match("RAIZ_ENESIMA"):
            operador = self.advance()
            derecha = self.raiz_y_potencia()

            if operador.tipo == "POTENCIA":
                return NodoPotencia(base, derecha)

            if operador.tipo == "RAIZ_ENESIMA":
                return NodoRaizEnesima(base, derecha)
        
        return base 

    def factor(self):
        if self.match("PAREN_IZQ"):
            self.advance()
            paren_tree = self.expr()
            if self.peek().tipo != "PAREN_DER":
                raise Exception(f"ERROR:No cerraste un parentesis:\nToken:{self.peek().valor}\nColumna:{self.peek().columna}")
            self.advance()
            return paren_tree
        
        elif self.match("SUMA"):
            self.advance()
            return NodoPositivo(self.raiz_y_potencia())
        
        elif self.match("RESTA"):
            self.advance()
            return NodoNegativo(self.raiz_y_potencia())
        
        elif self.match("NUMERO"):
            token = self.advance()
            return NodoNumero(token.valor)
        
        else:
            raise Exception(f"ERROR:Esperaba un número:\nToken:{self.peek().valor}\nColumna:{self.peek().columna}")
            
    
    

  

