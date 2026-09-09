from constantes import PALABRAS_RESERVADAS, OPERADORES_SIMPLES, OPERADORES_DOBLES

class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
        

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.limite = len(texto)
        self.puntero = 0
        self.linea = 1
        

    def advance(self):
        str_actual = self.texto[self.puntero]
        self.puntero += 1
        return str_actual
    
    def peek(self, pasos=0):
        return self.texto[self.puntero + pasos]
    
    def leer_palabra(self):
        buffer = ""
        while self.puntero < self.limite and (self.peek().isalnum() or self.peek() == "_"):
            buffer += self.advance()
        if buffer in PALABRAS_RESERVADAS:
            tipo_token = PALABRAS_RESERVADAS[buffer]
            return Token(tipo_token, buffer, self.linea, self.puntero)  
        return Token("IDENTIFICADOR", buffer, self.linea, self.puntero)    

    def leer_simbolo(self):
        if self.puntero < self.limite:
            if self.puntero < self.limite - 1 and self.peek() + self.peek(1) in OPERADORES_DOBLES:
                valor_token = self.advance()
                valor_token += self.advance()
                tipo_token = OPERADORES_DOBLES[valor_token]
            else:
                valor_token = self.advance()
                tipo_token = OPERADORES_SIMPLES[valor_token]
            return Token(tipo_token, valor_token, self.linea, self.puntero)   
            
    def leer_numero(self):
        contador_punto_decimal = 0
        buffer = ""
        while self.puntero < self.limite and (self.peek().isdigit() or self.peek() == "."):
            if self.peek() == ".":
                contador_punto_decimal += 1
            buffer += self.advance()
            
        if contador_punto_decimal > 1 or buffer == ".":
            return Token("ERROR", buffer, self.linea, self.puntero)
        
        if contador_punto_decimal:
            if buffer[0] == ".":
                buffer = "0" + buffer
            elif buffer[-1] == ".":
                buffer += "0"
            return Token("NUMERO", float(buffer), self.linea, self.puntero)
        return Token("NUMERO", int(buffer), self.linea, self.puntero)
        
    def tokenizar(self):
        tokens  = [] 
        
        while self.puntero < self.limite:
            char_actual = self.peek()

            if char_actual.isspace() or char_actual == "|":
                if char_actual == "|":
                    self.linea += 1
                self.advance()

            elif char_actual.isalpha() or char_actual == "_":
                tokens.append(self.leer_palabra())

            elif char_actual in OPERADORES_SIMPLES:
                tokens.append(self.leer_simbolo())

            elif char_actual.isdigit() or char_actual == ".":
                tokens.append(self.leer_numero())  

            else:
                tokens.append(Token("ERROR", char_actual, self.linea, self.puntero))
                self.advance()

        tokens.append(Token("FIN", None, self.linea, self.puntero + 1))
        return tokens



          