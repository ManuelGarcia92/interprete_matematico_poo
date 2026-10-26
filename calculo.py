from evaluacion import TablaDeSimbolos, evaluar_instrucciones
from parser import Parser
from lexer import Lexer
import readline
import consola

def calculo() -> None:
    texto = ""
    memoria = TablaDeSimbolos()
    while True:
        consola.limpiar_terminal()
        memoria.imprimir_memoria()
        consola.imprimir("Ingrese el comando [:break] para salir.")
        texto = consola.modificar_dato(">>> : ", texto)
        if texto.lower() == ":break":
            break
        if texto.strip() == "":
            continue
        try:
            texto = str(procesar_expresion(texto, memoria))
        except Exception as error:
            consola.imprimir(f"[Error de Ejecución]: {error}")     
        consola.pausa()

def procesar_expresion(texto: str, memoria: TablaDeSimbolos) -> int | float | None:
    lexer = Lexer(texto)
    tokens = lexer.tokenizar()
    parser = Parser(tokens)
    arbol = parser.parsear()
    resultado = evaluar_instrucciones(arbol, memoria)
    if resultado is None:
        resultado = ""
    return resultado