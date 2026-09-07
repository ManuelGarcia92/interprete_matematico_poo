from constantes import PALABRAS_RESERVADAS, OPERADORES_SIMPLES, OPERADORES_DOBLES

class Token:
    def __init__(self, tipo, valor, columna):
        self.tipo = tipo
        self.valor = valor
        self.columna = columna

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.puntero = 0
        self.limite = len(texto)

    def peek(self, pasos=0):
        return self.texto[self.puntero + pasos]
    
    def leer_palabra(self):
        buffer = ""
        while self.puntero < self.limite and (self.peek().isalnum() or self.peek() == "_"):
            buffer += self.peek()
            self.puntero += 1
            columna = self.puntero
        if buffer in PALABRAS_RESERVADAS:
            tipo_token = PALABRAS_RESERVADAS[buffer]
            return Token(tipo_token, buffer, columna)  
        return Token("IDENTIFICADOR", buffer, columna)    

    def leer_simbolo(self):
        if self.puntero < self.limite:

            if self.puntero < self.limite - 1 and self.peek() + self.peek(1) in OPERADORES_DOBLES:
                valor_token = self.peek() + self.peek(1)
                tipo_token = OPERADORES_DOBLES[valor_token]
                self.puntero += 2
                columna = self.puntero
            else:
                valor_token = self.peek()
                tipo_token = OPERADORES_SIMPLES[valor_token]
                self.puntero += 1  
                columna = self.puntero 
            return Token(tipo_token, valor_token, columna)   
            
    def leer_numero(self):
        contador_punto_decimal = 0
        buffer = ""

        while self.puntero < self.limite and (self.peek().isdigit() or self.peek() == "."):
            if self.peek() == ".":
                contador_punto_decimal += 1
            buffer += self.peek()
            self.puntero += 1
            columna = self.puntero

        if contador_punto_decimal > 1 or buffer == ".":
            return Token("ERROR", buffer, columna)
        
        if contador_punto_decimal:
            if buffer[0] == ".":
                buffer = "0" + buffer
            elif buffer[-1] == ".":
                buffer += "0"
            return Token("NUMERO", float(buffer), columna)
        return Token("NUMERO", int(buffer), columna)
        
    def tokenizar(self):
        tokens  = [] 
        
        while self.puntero < self.limite:
            char_actual = self.peek()

            if char_actual.isspace():
                self.puntero += 1

            elif char_actual.isalpha() or char_actual == "_":
                tokens.append(self.leer_palabra())

            elif char_actual in OPERADORES_SIMPLES:
                tokens.append(self.leer_simbolo())

            elif char_actual.isdigit() or char_actual == ".":
                tokens.append(self.leer_numero())  

            else:
                tokens.append(Token("ERROR", char_actual, self.puntero))
                self.puntero += 1

        tokens.append(Token("FIN", None, self.limite + 1))
        return tokens



          