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
            if resultado:
                mensaje_salida = resultado
            else:
                mensaje_salida = ""
        except Exception as error:
            mensaje_salida = f"[ERROR : {error}]"
       