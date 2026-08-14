class NodoBinario:
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha
        self.OPERACIONES = {
        "*" : lambda x, y: x * y,
        "/" : lambda x, y: x / y,
        "//": lambda x, y: x // y,
        "+" : lambda x, y: x + y,
        "-" : lambda x, y: x - y
        }

    def evaluar(self):
        return self.OPERACIONES[self.operador]((self.izquierda.evaluar()), (self.derecha.evaluar()))

class NodoNumero:
    def __init__(self, valor):
        self.valor = valor

    def evaluar(self):
        return float(self.valor)

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
        nodo = self.factor()
        while self.match("MULTIPLICACION") or self.match("DIVISION") or self.match("DIVI_ENTERA"):
            operador = self.advance()
            derecha = self.factor()
            nodo = NodoBinario(nodo, operador.valor, derecha)
        return nodo   
    
    def factor(self):
        if self.match("NUMERO"):
            token = self.advance()
            return NodoNumero(token.valor)
        else:
            raise Exception("Esperaba un número")
            
    
    

  

