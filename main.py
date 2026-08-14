from lexer import Lexer 
from parser import Parser
texto = "2*3+2+2*3/2/2*42/2+4-45"
lexer = Lexer(texto)
tokens = lexer.tokenizar()
parser = Parser(tokens)
try:
    arbol = parser.expr()
    resultado = arbol.evaluar()
    print(resultado)
except Exception as error:
    print(error)


