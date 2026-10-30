from editor import Editor
from interprete import procesar_instrucciones

def iniciar_consola() -> None:
    mensaje_salida = ""
    editor = Editor()
    while True:
        matriz = editor.salida(mensaje_inferior=mensaje_salida)
        texto = editor.formatear_matriz(matriz)
        if not editor.procesar:
            break
        try:
            resultado = procesar_instrucciones(texto)
            mensaje_salida = editor.formatear_salida(resultado)
        except Exception as error:
            mensaje_salida = f"[ERROR : {error}]"
       