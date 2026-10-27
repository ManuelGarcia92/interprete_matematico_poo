from evaluacion import TablaDeSimbolos, evaluar_instrucciones
from parser import Parser
from editor import Editor
from lexer import Lexer
import readline

def calculo() -> None:
    mensaje_abajo = "Resultado = "
    editor = Editor()
    while True:
        matriz = editor.salida(
            mensaje_superior="[Presione [Escape] para salir]\n[Presione [Control+R] para procesar]",
            mensaje_inferior=mensaje_abajo
        )
        texto = editor.formatear_matriz(matriz)

        if not editor.procesar:
            break

        if texto.strip() == "":
            continue
        try:
            mensaje_abajo = f"Resultado = {procesar_expresion(texto)}"
        except Exception as error:
            mensaje_abajo = error
       
def procesar_expresion(texto: str) -> int | float | str:
    memoria = TablaDeSimbolos()
    lexer = Lexer(texto)
    tokens = lexer.tokenizar()
    parser = Parser(tokens)
    arbol = parser.parsear()
    resultado = evaluar_instrucciones(arbol, memoria)
    if resultado is None:
        resultado = ""
    return resultado