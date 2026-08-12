class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.puntero = 0
        self.limite = len(texto)
        self.PALABRAS_RESERVADAS = {
            "int": "TIPO_INIT",
            "float": "TIPO_FLOAT",
            "bool": "TIPO_BOOL",
            "return": "RESERVADA_RETURN"
        }
        self.OPERADORES_SIMPLES = {
            "+": "SUMA",
            "-": "RESTA",
            "*": "MULTIPLICACION",
            "/": "DIVISION",
            "=": "ASIGNACION",
            ":": "DOP_PUNTOS",
            ";": "PUNTO_Y_COMA",
            "|": "SEPARACION",
            "(": "PAREN_IZQ",
            ")": "PAREN_DER"
        }
        self.OPERADORES_DOBLES = {
            "**": "POTENCIA",
            "//": "DIV_ENTERA",
            "||": "DELIMITACION"
        }

    def leer_palabra(self):
        buffer = ""
        while self.puntero < self.limite and (self.texto[self.puntero].isalnum() or self.texto[self.puntero] == "_"):
            buffer += self.texto[self.puntero]
            self.puntero += 1
        if buffer in self.PALABRAS_RESERVADAS:
            tipo_token = self.PALABRAS_RESERVADAS.get(buffer)
        else:
            tipo_token = "IDENTIFICADOR"
        return Token(tipo_token, buffer)    

    def leer_simbolo(self):
        if self.puntero < self.limite:
            simbolo_doble = self.texto[self.puntero] + self.texto[self.puntero + 1]
            if simbolo_doble in self.OPERADORES_DOBLES:
                self.puntero += 2
                return Token(self.OPERADORES_DOBLES[simbolo_doble], simbolo_doble)
            
        simbolo_actual = self.texto[self.puntero]
        if simbolo_actual in self.OPERADORES_SIMPLES:
            self.puntero += 1
            return Token(self.OPERADORES_SIMPLES[simbolo_actual], simbolo_actual)
            
    def leer_numero(self):
        contador_punto_decimal = 0
        buffer = ""
        while self.puntero < self.limite and (self.texto[self.puntero].isdigit() or self.texto[self.puntero] == "."):
            if self.texto[self.puntero] == ".":
                contador_punto_decimal += 1
            buffer += self.texto[self.puntero]
            self.puntero += 1
        if contador_punto_decimal <= 1:
            if buffer == ".":
                return Token("ERROR", buffer)
            elif "." in buffer[0]:
                buffer = "0" + buffer
            elif "." in buffer[-1]:
                buffer += "0"
            return Token("NUMERO", buffer)
        else:
            return Token("ERROR", buffer)
    
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
        return tokens
    
while True:
    texto = input(">>> : ")
    if texto == "xyz":
        break
    lexer = Lexer(texto)
    lista_tokens = lexer.tokenizar()
    print(texto)
    for t in lista_tokens:
        print(f"Tipo: {t.tipo}, Valor: {t.valor}")



          