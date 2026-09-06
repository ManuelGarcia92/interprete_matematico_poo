from tabla_de_simbolos import TablaDeSimbolos
from lexer import Lexer 
from parser import Parser
from interprete import Interprete

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
        memoria = TablaDeSimbolos()
        lexer = Lexer(texto)
        tokens = lexer.tokenizar()
        parser = Parser(tokens)
        arbol = parser.parsear()
        interprete = Interprete(arbol)
        resultado = interprete.evaluar(memoria)
        if resultado:
            print(resultado)
        else:
            print()

    except Exception as error:
        print(error)

    input("Presione ENTER para continuar...")


