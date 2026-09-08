import nodos

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.limite = len(tokens)
        self.puntero = 0
        self.errores = ""

    def levantar_error(self, mensaje, pasos=0):
        self.errores += f"Error: {mensaje}: Token: {self.peek(pasos).valor} Columna: {self.peek(pasos).columna}\n"

    def advance(self, pasos=1):
        if self.puntero + pasos < self.limite:
            token = self.tokens[self.puntero]
            self.puntero += pasos
            return token
        return None
    
    def peek(self, pasos=0):
        if self.puntero + pasos < self.limite:
            return self.tokens[self.puntero + pasos]
        return None
    
    def match(self, tipo, pasos=0):
        token = self.peek(pasos)
        return token is not None and token.tipo == tipo
    
    def consumir(self, tipo, mensaje_error):
        if self.match(tipo):
            return self.advance()
        self.levantar_error(mensaje_error)
        return None
    
    def parsear(self):
        arbol = []

        if self.match("FIN"):
            raise Exception("Expresión vacia")
        
        while not self.match("FIN") and not self.match("LLAVE_DER"):
            arbol.append(self.parsear_instrucciones())

            if self.match("PUNTO_Y_COMA"):
                self.advance()
            else:
                break

        if self.peek() and self.peek().tipo != "FIN" and not self.match("LLAVE_DER"):
            self.levantar_error("Quedan tokens sin procesar")

        if self.errores:
            raise Exception(self.errores)
        
        return arbol
        
    def parsear_instrucciones(self):
        if self.puntero < self.limite - 1 and self.match("IDENTIFICADOR") and self.match("ASIGNACION", 1):
            token_id = self.advance()
            self.advance()
            nombre_id = token_id.valor
            nodo_expr = self.expr()
            return nodos.NodoAsignacion(nombre_id, nodo_expr)
            
        elif self.match("DEF"):
            self.advance()
            token_nombre = self.consumir("IDENTIFICADOR", "Se esperaba el nombre de la función")
            self.consumir("PAREN_IZQ", "Los argumentos de una función deben estar entre paréntesis : ( )")
            argumentos = self.parsear_argumentos()
            self.consumir("LLAVE_IZQ", "El cuerpo de una función debe estar definido dentro de llaves : { }")
            cuerpo = self.parsear()
            self.consumir("LLAVE_DER", "No cerraste la llave : }")
            nombre = token_nombre.valor if token_nombre else "error"
            return nodos.NodoFuncion(nombre, argumentos, cuerpo)
        
        elif self.match("RETURN"):
            self.advance()
            return nodos.NodoReturn(self.expr())
    
        else:
            return self.expr()
        
    def parsear_argumentos(self):
        argumentos = []
        if not self.match("PAREN_DER"):
            argumentos.append(self.expr())
            while self.match("COMA"):
                self.advance()
                argumentos.append(self.expr())
                
        self.consumir("PAREN_DER", "Falta el paréntesis de cierre ) en los argumentos")
        return argumentos
    
    def expr(self):
        nodo = self.term()
        while self.match("SUMA") or self.match("RESTA"):
            operador = self.advance()
            derecha = self.term()
            if operador.tipo == "SUMA":
                nodo = nodos.NodoSuma(nodo, derecha)
            else:
                nodo = nodos.NodoResta(nodo, derecha)
        return nodo
    
    def term(self):
        nodo = self.power()

        while self.match("MULTI") or self.match("DIV") or self.match("DIV_ENTERA") or self.match("MOD"):
            operador = self.advance()
            derecha = self.power()
            if operador.tipo == "MULTI":
                nodo = nodos.NodoMulti(nodo, derecha)
            elif operador.tipo == "DIV":
                nodo = nodos.NodoDiv(nodo, derecha)
            elif operador.tipo == "DIV_ENTERA":
                nodo = nodos.NodoDivEntera(nodo, derecha)
            else:
                nodo = nodos.NodoModulo(nodo, derecha)
        return nodo   
    
    def power(self):
        nodo = self.factor()
        if self.match("POTENCIA") or self.match("RAIZ_ENESIMA"):
            operador = self.advance()
            derecha = self.power()
            if operador.tipo == "POTENCIA":
                return nodos.NodoPotencia(nodo, derecha)
            else: 
                return nodos.NodoRaizEnesima(nodo, derecha)
        return nodo 
    
    def factor(self):
        if self.match("PAREN_IZQ"):
            self.advance()
            nodo_expr = self.expr()
            self.consumir("PAREN_DER", "No cerraste un paréntesis")
            return nodo_expr
        
        if self.match("SUMA") or self.match("RESTA"):
            if self.match("SUMA", 1) or self.match("RESTA", 1):
                self.levantar_error("Operador repetido", 1)
            operador = self.advance()
            if operador.tipo == "SUMA":
                return nodos.NodoPositivo(self.power())
            else:
                return nodos.NodoNegativo(self.power())
            
        funciones_nativas = {
            "ABS"  : nodos.NodoAbs,  "SIN"  : nodos.NodoSin,  "ASIN" : nodos.NodoAsin,
            "COS"  : nodos.NodoCos,  "ACOS" : nodos.NodoAcos, "TAN"  : nodos.NodoTan,
            "ATAN" : nodos.NodoAtan, "LOG"  : nodos.NodoLog
        }

        token_actual = self.peek()
        if token_actual and token_actual.tipo in funciones_nativas:
            self.advance()
            operacion = self.factor()
            return funciones_nativas[token_actual.tipo](operacion)
        
        if self.match("NUMERO"):
            token = self.advance()
            return nodos.NodoNumero(token.valor)
        
        if self.match("IDENTIFICADOR"):
            token = self.advance()
            if self.match("PAREN_IZQ"):
                self.advance()
                argumentos = self.parsear_argumentos()
                return nodos.NodoLlamada(token.valor, argumentos)
            return nodos.NodoIdentificador(token.valor)
        
        self.levantar_error("Esperaba un número")
        return None
            
            
    
    

  

