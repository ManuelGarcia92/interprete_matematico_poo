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
    
    def parsear(self):
        trees = []

        if self.match("FIN"):
            raise Exception("Expresión vacia")
        
        while not self.match("FIN"):
            if self.match("LLAVE_DER"):
                break

            if self.puntero < self.limite - 1 and self.match("IDENTIFICADOR") and self.match("ASIGNACION", 1):
                token = self.advance(2)
                nodo = self.expr()
                asign_tree = nodos.NodoAsignacion(token.valor, nodo)
                trees.append(asign_tree)

            elif self.puntero < self.limite - 1 and self.match("DEF") and self.match("IDENTIFICADOR", 1):
                self.advance()
                token = self.advance()
                nombre = token.valor

                if not self.match("PAREN_IZQ"):
                    self.levantar_error("Los argumentos de una función deben estar entre parentesis : ( )")

                else:
                    self.advance()
                    argumentos = self.parsear_argumentos()

                    if not self.match("LLAVE_IZQ"):
                        self.levantar_error("El cuerpo de una función debe estar definido dentro de llaves : { }")

                    else:
                        self.advance()
                        codigo = self.parsear()

                        if not self.match("LLAVE_DER"):
                            self.levantar_error("No cerraste la llave : }")
            
                        else:
                            self.advance()
                            func_tree = nodos.NodoFuncion(nombre, argumentos, codigo)
                            trees.append(func_tree)
                    
            elif self.match("RETURN"):
                self.advance()
                expresion = self.expr()
                trees.append(nodos.NodoReturn(expresion))

            else:
                trees.append(self.expr())

            if self.match("PUNTO_Y_COMA"):
                self.advance()

            else:
                break

        if self.peek().tipo != "FIN" and not self.match("LLAVE_DER"):
            self.levantar_error("Quedan tokens sin procesar")

        if self.errores:
            raise Exception(self.errores)
        
        return trees
    
    def parsear_argumentos(self):
        argumentos = []

        if not self.match("PAREN_DER"):
            argumentos.append(self.expr())

            while self.match("COMA"):
                self.advance()
                argumentos.append(self.expr())
                
        if not self.match("PAREN_DER"):        
            self.levantar_error("Falta el paréntesis de cierre ) en los argumentos")

        else:
            self.advance()

        return argumentos
    
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

            elif operador.tipo == "MOD":
                nodo = nodos.NodoModulo(nodo, derecha)

        return nodo   
    
    def power(self):
        nodo = self.factor()

        if self.match("POTENCIA") or self.match("RAIZ_ENESIMA"):
            operador = self.advance()
            derecha = self.power()

            if operador.tipo == "POTENCIA":
                return nodos.NodoPotencia(nodo, derecha)

            if operador.tipo == "RAIZ_ENESIMA":
                return nodos.NodoRaizEnesima(nodo, derecha)
        
        return nodo 
    
    def factor(self):
        if self.match("PAREN_IZQ"):
            self.advance()
            paren_tree = self.expr()

            if not self.match("PAREN_DER"):
                self.levantar_error("No cerraste un parentesis")

            else:
                self.advance()

            return paren_tree
        
        elif self.match("SUMA") or self.match("RESTA"):
            if self.match("SUMA", 1) or self.match("RESTA", 1):
                self.levantar_error("Operador repetido", 1)

            operador = self.advance()

            if operador.tipo == "SUMA":
                return nodos.NodoPositivo(self.power())
            
            elif operador.tipo == "RESTA":
                return nodos.NodoNegativo(self.power())
            
        elif self.match("ABS"):
            self.advance()
            operacion = self.factor()
            return nodos.NodoAbs(operacion)  
          
        elif self.match("SIN"):
            self.advance()
            operacion = self.factor()
            return nodos.NodoSin(operacion)

        elif self.match("ASIN"):
            self.advance()
            operacion = self.factor()
            return nodos.NodoAsin(operacion)
        
        elif self.match("COS"):
            self.advance()
            operacion = self.factor()
            return nodos.NodoCos(operacion)
        
        elif self.match("ACOS"):
            self.advance()
            operacion = self.factor()
            return nodos.NodoAcos(operacion)
        
        elif self.match("TAN"):
            self.advance()
            operacion = self.factor()
            return nodos.NodoTan(operacion)

        elif self.match("ATAN"):
            self.advance()
            operacion = self.factor()
            return nodos.NodoAtan(operacion)
        
        elif self.match("LOG"):
            self.advance()
            operacion = self.factor()
            return nodos.NodoLog(operacion)
        
        elif self.match("NUMERO"):
            token = self.advance()
            return nodos.NodoNumero(token.valor)
        
        elif self.match("IDENTIFICADOR"):
            token = self.advance()
            if self.match("PAREN_IZQ"):
                self.advance()
                argumentos = self.parsear_argumentos()
                return nodos.NodoLlamada(token.valor, argumentos)
            return nodos.NodoIdentificador(token.valor)
        
        else:
            self.levantar_error("Esperaba un número")
            
            
    
    

  

