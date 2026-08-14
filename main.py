from lexer import Lexer 
from parser import Parser
while True:
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


