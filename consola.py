from prompt_toolkit import prompt

def limpiar_terminal() -> None:
    import os
    os.system("cls" if os.name == "nt" else "clear")

def pausa() -> None:
    input("Presione ENTER para continuar...")

def pedir_dato(mensaje: str) -> str:
    return input(mensaje)

def modificar_dato(mensaje, dato: str) -> str:
    return prompt(mensaje, default=dato)

def imprimir(mensaje: str) -> None:
    print(mensaje)

def imprimir_error(mensaje: str) -> None:
    print(f"ERROR: {mensaje}")



