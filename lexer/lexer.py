from .constantes_lexer import PALABRAS_RESERVADAS, OPERADORES_SIMPLES, OPERADORES_DOBLES
from .tokens import Token

class Lexer:
    def __init__(self, texto: str):
        self.texto = texto
        self.pos = 0
        self.linea = 1
        self.columna = 0

    def _avanzar(self) -> str:
        caracter = self.texto[self.pos]
        self.pos += 1
        self.columna += 1
        return caracter
                
    def _mirar(self, pasos=0) -> str:
        return self.texto[self.pos + pasos]
    
    def _leer_numero(self) -> Token:
        col_inicio = self.columna + 1
        contador_de_puntos_decimales = 0
        buffer = ""
        while self.pos < len(self.texto) and (self._mirar().isdigit() or self._mirar() == "."):
            if self._mirar() == ".":
                contador_de_puntos_decimales += 1
            buffer += self._avanzar()
        col_fin = self.columna
        if contador_de_puntos_decimales > 1:
            raise Exception(f"Número con varios puntos decimales : {buffer}")
        return Token("NUMERO", buffer, self.linea, f"{col_inicio}-{col_fin}")

    def _leer_simbolo(self) -> Token:
        if self.pos < len(self.texto):
            col_inicio = self.columna + 1
            if self.pos < len(self.texto) - 1 and self._mirar() + self._mirar(1) in OPERADORES_DOBLES:
                valor_token = self._avanzar()
                valor_token += self._avanzar()
                tipo_token = OPERADORES_DOBLES[valor_token]
            else:
                valor_token = self._avanzar()
                tipo_token = OPERADORES_SIMPLES[valor_token]
            col_fin = self.columna
            return Token(tipo_token, valor_token, self.linea, f"{col_inicio}-{col_fin}")

    def _leer_palabra(self) -> Token:
        buffer = ""
        col_inicio = self.columna + 1
        while self.pos < len(self.texto) and (self._mirar().isalnum() or self._mirar() == "_"):
            buffer += self._avanzar()
        if buffer in PALABRAS_RESERVADAS:
            tipo_token = PALABRAS_RESERVADAS[buffer] 
        else:
            tipo_token = "IDENTIFICADOR"
        col_fin = self.columna
        return Token(tipo_token, buffer, self.linea, f"{col_inicio}-{col_fin}")

    def tokenizar(self) -> list:
        tokens  = [] 
        while self.pos < len(self.texto):
            caracter_actual = self._mirar()
            if caracter_actual.isspace():
                self._avanzar()
            elif caracter_actual == "|":
                self._avanzar()
                self.linea += 1
                self.columna = 0
            elif caracter_actual.isalpha() or caracter_actual == "_":
                tokens.append(self._leer_palabra())
            elif caracter_actual in OPERADORES_SIMPLES:
                tokens.append(self._leer_simbolo())
            elif caracter_actual.isdigit() or caracter_actual == ".":
                tokens.append(self._leer_numero())  
            else:
                raise Exception(f"Caracter desconocido : {caracter_actual}")
        col = self.columna + 1
        tokens.append(Token("FIN", "Fin", self.linea, f"{col}-{col}"))
        return tokens