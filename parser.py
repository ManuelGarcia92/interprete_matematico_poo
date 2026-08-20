import nodos
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.errores = ""
        self.puntero = 0
        self.limite = len(tokens)

    def advance(self, pasos=1):
        token = self.tokens[self.puntero]
        self.puntero += pasos
        return token
    
    def peek(self, pasos=0):
        if self.puntero + pasos < self.limite:
            return self.tokens[self.puntero + pasos]
        return None
    
    def match(self, tipo, pasos=0):
        token = self.peek(pasos)
        return token is not None and token.tipo == tipo
    
    def parsear(self):
        trees = []
        if self.match("FIN"):
            raise Exception("Expresión vacia")
        
        while not self.match("FIN"):
            if self.puntero < self.limite - 1 and self.match("IDENTIFICADOR") and self.match("ASIGNACION", 1):
                token = self.advance()
                self.advance()
                nodo = self.expr()
                asign_tree = nodos.NodoAsignacion(token.valor, nodo)
                trees.append(asign_tree)

            else:
                trees.append(self.expr())

            if self.match("PUNTO_Y_COMA"):
                self.advance()

            else:
                break

        if self.peek().tipo != "FIN":
            self.errores += f"ERROR: Quedan tokens sin procesar: Token: {self.peek().valor} Columna: {self.peek().columna}\n"

        if self.errores:
            raise Exception(self.errores)
        
        return trees

    def expr(self):
        nodo = self.term()

        while self.match("SUMA") or self.match("RESTA"):
            operador = self.advance()
            derecha = self.term()

            if operador.tipo == "SUMA":
                nodo = nodos.NodoSuma(nodo, derecha)

            elif operador.tipo == "RESTA":
                nodo = nodos.NodoResta(nodo, derecha)

        return nodo
    
    def term(self):
        nodo = self.raiz_y_potencia()

        while self.match("MULTI") or self.match("DIV") or self.match("DIV_ENTERA"):
            operador = self.advance()
            derecha = self.raiz_y_potencia()

            if operador.tipo == "MULTI":
                nodo = nodos.NodoMulti(nodo, derecha)

            elif operador.tipo == "DIV":
                nodo = nodos.NodoDiv(nodo, derecha)

            elif operador.tipo == "DIV_ENTERA":
                nodo = nodos.NodoDivEntera(nodo, derecha)

        return nodo   
    
    def raiz_y_potencia(self):
        base = self.factor()

        if self.match("POTENCIA") or self.match("RAIZ_ENESIMA"):
            operador = self.advance()
            derecha = self.raiz_y_potencia()

            if operador.tipo == "POTENCIA":
                return nodos.NodoPotencia(base, derecha)

            if operador.tipo == "RAIZ_ENESIMA":
                return nodos.NodoRaizEnesima(base, derecha)
        
        return base 

    def factor(self):
        if self.match("PAREN_IZQ"):
            self.advance()
            paren_tree = self.expr()

            if not self.match("PAREN_DER"):
                self.errores += f"ERROR: No cerraste un parentesis: Token: {self.peek().valor} Columna: {self.peek().columna}\n"

            else:
                self.advance()

            return paren_tree
        
        elif self.match("SUMA"):
            self.advance()
            return nodos.NodoPositivo(self.raiz_y_potencia())
        
        elif self.match("RESTA"):
            self.advance()
            return nodos.NodoNegativo(self.raiz_y_potencia())
        
        elif self.match("NUMERO"):
            token = self.advance()
            return nodos.NodoNumero(token.valor)
        
        elif self.match("IDENTIFICADOR"):
            token = self.advance()
            return nodos.NodoIdentificador(token.valor)
        
        else:
            self.errores += f"ERROR: Esperaba un número: Token: {self.peek().valor} Columna: {self.peek().columna}\n"
            
    
    

  

