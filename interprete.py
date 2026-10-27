from evaluacion import TablaDeSimbolos, evaluar_instrucciones
from lexer import Lexer
from parser import Parser

def procesar_instrucciones(texto: str) -> int | float | str:
    memoria = TablaDeSimbolos()
    lexer = Lexer(texto)
    tokens = lexer.tokenizar()
    parser = Parser(tokens)
    arbol = parser.parsear()
    resultado = evaluar_instrucciones(arbol, memoria)
    if resultado is None:
        resultado = ""
    return resultado