from extras import limpiar_terminal, pausa
from tabla_de_simbolos import TablaDeSimbolos
from lexer import Lexer 
from parser import Parser
from evaluador import Evaluador

def main():
    memoria = TablaDeSimbolos()

    while True:
        limpiar_terminal()
        print("[Ingrese break para salir]")
        texto = input(">>>: ")
        if texto == "break":
            break
        try:
            lexer = Lexer(texto)
            tokens = lexer.tokenizar()
            parser = Parser(tokens)
            arbol = parser.parsear()
            evaluador = Evaluador(arbol)
            resultado = evaluador.evaluar(memoria)
            if resultado:
                print(resultado)
            else:
                print()
        except Exception as error:
            print(error)     
        pausa()
        
if __name__ == "__main__":
    main()