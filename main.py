from lexer import Lexer 
from parser import Parser

def limpiar_terminal() -> None:
    import os
    os.system("cls" if os.name == "nt" else "clear")

while True:
    limpiar_terminal()
    print("[Ingrese xyz para salir.]")
    texto = input(">>> : ")
    if texto == "xyz":
        break
    lexer = Lexer(texto)
    tokens = lexer.tokenizar()
    parser = Parser(tokens)
    try:
        arbol = parser.expr()
        resultado = arbol.evaluar()
        print(resultado)
    except Exception as error:
        print(error)
    input()


