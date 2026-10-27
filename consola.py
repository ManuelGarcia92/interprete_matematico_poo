from evaluacion import TablaDeSimbolos, evaluar_instrucciones
from parser import Parser
from editor import Editor
from lexer import Lexer

def iniciar_consola() -> None:
    mensaje_salida = ""
    editor = Editor()
    while True:
        matriz = editor.salida(mensaje_inferior=mensaje_salida)
        texto = editor.formatear_matriz(matriz)

        if not editor.procesar:
            break

        if texto.strip() == "":
            continue
        
        try:
            mensaje_salida = f"Resultado = {procesar_instrucciones(texto)}"
        except Exception as error:
            mensaje_salida = f"[ERROR : {error}]"
       
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