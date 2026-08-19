from tabla_de_simbolos import TablaDeSimbolos
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
    try:
        lexer = Lexer(texto)
        tokens = lexer.tokenizar()
        parser = Parser(tokens)
        arbol = parser.parsear()
        resultado = arbol.evaluar()
        print(resultado)
    except Exception as error:
        print(error)
    input("Presione ENTER para continuar...")


