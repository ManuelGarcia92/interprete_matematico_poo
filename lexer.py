class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.puntero = 0
        self.limite = len(texto)
        self.OPERADORES_SIMPLES = {
            "+": "SUMA",
            "-": "RESTA",
            "*": "MULTIPLICACION",
            "/": "DIVISION"
        }
        self.OPERADORES_DOBLES = {
            "**": "POTENCIA",
            "//": "DIV_ENTERA"
        }

    def leer_palabra(self):
        buffer = ""
        while self.puntero < self.limite and (self.texto[self.puntero].isalnum() or self.texto[self.puntero] == "_"):
            buffer += self.texto[self.puntero]
            self.puntero += 1
        return Token("IDENTIFICADOR", buffer)    

    def leer_simbolo(self):
        if self.puntero < self.limite:
            if self.puntero < self.limite - 1 and self.texto[self.puntero] + self.texto[self.puntero + 1] in self.OPERADORES_DOBLES:
                valor_token = self.texto[self.puntero] + self.texto[self.puntero + 1]
                tipo_token = self.OPERADORES_DOBLES[valor_token]
                self.puntero += 2
            else:
                valor_token = self.texto[self.puntero]
                tipo_token = self.OPERADORES_SIMPLES[valor_token]
                self.puntero += 1     
            return Token(tipo_token, valor_token)   
            
    def leer_numero(self):
        contador_punto_decimal = 0
        buffer = ""
        while self.puntero < self.limite and (self.texto[self.puntero].isdigit() or self.texto[self.puntero] == "."):
            if self.texto[self.puntero] == ".":
                contador_punto_decimal += 1
            buffer += self.texto[self.puntero]
            self.puntero += 1
        if contador_punto_decimal > 1 or buffer == ".":
            return Token("ERROR", buffer)
        elif buffer[0] == ".":
            buffer = "0" + buffer
        elif buffer[-1] == ".":
            buffer += "0"
        return Token("NUMERO", buffer)
      
    def tokenizar(self):
        tokens  = [] 
        while self.puntero < self.limite:
            char_actual = self.texto[self.puntero]
            if char_actual.isspace():
                self.puntero += 1
            elif char_actual.isalpha() or char_actual == "_":
                tokens.append(self.leer_palabra())
            elif char_actual in self.OPERADORES_SIMPLES:
                tokens.append(self.leer_simbolo())
            elif char_actual.isdigit() or char_actual == ".":
                tokens.append(self.leer_numero())          
            else:
                tokens.append(Token("ERROR", char_actual))
                self.puntero += 1
        tokens.append(Token("FIN", None))
        return tokens
    





          