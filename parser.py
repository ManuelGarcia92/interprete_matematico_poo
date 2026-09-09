import nodos

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.limite = len(tokens)
        self.puntero = 0
        self.errores = ""

    def levantar_error(self, mensaje, pasos=0):
        self.errores += f"Error: {mensaje}: Token: {self.peek(pasos).valor} Linea: {self.peek(pasos).linea} Columna: {self.peek(pasos).columna}\n"

    def advance(self):
        if self.puntero < self.limite:
            token = self.tokens[self.puntero]
            self.puntero += 1
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
    
    def sincronizar(self):
        while not self.match("FIN"):
            if self.peek(-1) and self.peek(-1).tipo == "PUNTO_Y_COMA":
                return
            if self.match("DEF") or self.match("RETURN") or self.match("IDENTIFICADOR"):
                return
            self.advance()

    def parsear(self):
        instrucciones = []

        if self.match("FIN"):
            raise Exception("Expresión vacia")
        
        while not self.match("FIN") and not self.match("LLAVE_DER"):
            instruccion = self.parsear_instrucciones()

            if instruccion is not None:
                instrucciones.append(instruccion)

                if self.match("PUNTO_Y_COMA"):
                    self.advance()
            else:
                self.levantar_error("Sintaxis erronea")
                self.sincronizar()

        if self.peek() and not self.match("FIN") and not self.match("LLAVE_DER"):
            self.levantar_error("Quedan tokens sin procesar")
            return None

        if self.errores:
            raise Exception(self.errores)
        
        return instrucciones
        
    def parsear_instrucciones(self):
        if self.puntero < self.limite - 1 and self.match("IDENTIFICADOR") and self.match("ASIGNACION", 1):
            token_id = self.advance()
            self.advance()
            nodo_expr = self.expr()
            return nodos.NodoAsignacion(token_id.valor, nodo_expr)
            
        elif self.match("DEF"):
            self.advance()
            token_id = self.consumir("IDENTIFICADOR", "Se esperaba el nombre de la función")
            self.consumir("PAREN_IZQ", "Los argumentos de una función deben estar entre paréntesis : ( )")
            argumentos = self.parsear_argumentos()
            self.consumir("LLAVE_IZQ", "El cuerpo de una función debe estar definido dentro de llaves : { }")
            cuerpo = self.parsear()
            self.consumir("LLAVE_DER", "No cerraste la llave : }")
            return nodos.NodoFuncion(token_id.valor, argumentos, cuerpo)
        
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
            operador = self.advance()

            if self.match("SUMA") or self.match("RESTA"):
                self.levantar_error("Operador repetido")
                return None
            
            if operador.tipo == "SUMA":
                return nodos.NodoPositivo(self.power())
            else:
                return nodos.NodoNegativo(self.power())
        
        if self.match("NUMERO"):
            token = self.advance()
            return nodos.NodoNumero(token.valor)
        
        if self.match("IDENTIFICADOR"):
            token_id = self.advance()
            if self.match("PAREN_IZQ"):
                self.advance()
                argumentos = self.parsear_argumentos()
                return nodos.NodoLlamada(token_id.valor, argumentos)
            return nodos.NodoIdentificador(token_id.valor)
        
        self.levantar_error("Esperaba un número")
        return None
            
            
    
    

  

