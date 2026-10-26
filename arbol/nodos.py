from evaluacion import evaluar_instrucciones
from .despacho import OPERACIONES

class NodoNumero:
    def __init__(self, valor):
        self.valor = valor

    def evaluar(self, memoria):
        if "." in self.valor:
            valor = float(self.valor)
        else:
            valor = int(self.valor)
        return valor

class NodoUnario:
    def __init__(self, signo : str, valor):
        self.signo = signo
        self.valor = valor

    def evaluar(self, memoria):
        resultado = self.valor.evaluar(memoria)
        if self.signo == "-":
            return -resultado
        else:
            return resultado
        
class NodoBinario:
    def __init__(self, operador : str, nodo_izquierdo, nodo_derecho):
        self.operador = operador
        self.nodo_izquierdo = nodo_izquierdo
        self.nodo_derecho = nodo_derecho
    
    def evaluar(self, memoria):
        valor_izquierda = self.nodo_izquierdo.evaluar(memoria)
        valor_derecha = self.nodo_derecho.evaluar(memoria)
        return OPERACIONES[self.operador](valor_izquierda, valor_derecha)

class NodoDeclararVar:
    def __init__(self, nombre : str, valor):
        self.nombre = nombre
        self.valor = valor

    def evaluar(self, memoria):
        return memoria.declarar_variable(self.nombre, self.valor.evaluar(memoria))

class NodoDeclararFun:
    def __init__(self, nombre : str, argumentos : list, cuerpo : list):
        self.nombre = nombre
        self.argumentos = argumentos
        self.cuerpo = cuerpo

    def evaluar(self, memoria):
        memoria.declarar_funcion(self.nombre, self.argumentos, self.cuerpo)

class NodoEliminacion:
    def __init__(self, nombre : str):
        self.clave = nombre

    def evaluar(self, memoria):
        return memoria.eliminar(self.clave)
    
class NodoLlamarVar:
    def __init__(self, nombre : str):
        self.nombre = nombre

    def evaluar(self, memoria):
        return memoria.llamar_variable(self.nombre)
    
class NodoLlamarFun:
    def __init__(self, nombre : str, argumentos : list):
        self.nombre = nombre
        self.argumentos = argumentos

    def evaluar(self, memoria):
        func = memoria.llamar_funcion(self.nombre)
        param_nombres = func["argumentos"]
        cuerpo_codigo = func["cuerpo"]
        valores = [arg.evaluar(memoria) for arg in self.argumentos]
        entorno_local = memoria.crear_entorno_local()
        for param, valor in zip(param_nombres, valores):
            entorno_local.declarar_variable(param.nombre, valor)
        resultado = evaluar_instrucciones(cuerpo_codigo, entorno_local)
        return resultado           