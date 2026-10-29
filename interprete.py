from evaluacion import TablaDeSimbolos, evaluar_instrucciones
from lexer import Lexer
from parser import Parser

def procesar_instrucciones(texto: str) -> int | float | None:
    memoria = TablaDeSimbolos()
    lexer = Lexer(texto)
    tokens = lexer.tokenizar()
    parser = Parser(tokens)
    arbol = parser.parsear()
    resultado = evaluar_instrucciones(arbol, memoria)
    return resultado