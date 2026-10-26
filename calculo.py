from evaluacion import TablaDeSimbolos, evaluar_instrucciones
from parser import Parser
from editor import Editor
from lexer import Lexer
import readline

def calculo() -> None:
    mensaje_abajo = "Resultado = "
    editor = Editor()
    while True:
        texto = editor.formatear_matriz(editor.salida(
            mensaje_superior="[Ingrese el comando [:break] para salir.]",
            mensaje_inferior=mensaje_abajo
        ))

        if texto.lower() == ":break":
            break
        if texto.strip() == "":
            continue
        try:
            resultado_operacion = procesar_expresion(texto)
            mensaje_abajo = f"Resultado = {resultado_operacion}"
        except Exception as error:
            mensaje_abajo = f"[Error de Ejecución]: {error}"
       
def procesar_expresion(texto: str) -> int | float | None:
    memoria = TablaDeSimbolos()
    lexer = Lexer(texto)
    tokens = lexer.tokenizar()
    parser = Parser(tokens)
    arbol = parser.parsear()
    resultado = evaluar_instrucciones(arbol, memoria)
    if resultado is None:
        resultado = ""
    return resultado