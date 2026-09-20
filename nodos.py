from constantes import OPERACIONES
class NodoBinario:
    def __init__(self, operador, izquierda, derecha):
        self.operador = operador
        self.izquierda = izquierda
        self.derecha = derecha
    
    def evaluar(self, memoria):
        valor_izquierda = self.izquierda.evaluar(memoria)
        valor_derecha = self.derecha.evaluar(memoria)
        resultado = OPERACIONES[self.operador](valor_izquierda, valor_derecha)
        return resultado
        
class NodoNumero:
    def __init__(self, valor):
        self.valor = valor

    def evaluar(self, memoria):
        return self.valor

class NodoPositivo(NodoNumero):
    def evaluar(self, memoria):
        return self.valor.evaluar(memoria)
    
class NodoNegativo(NodoNumero):
    def evaluar(self, memoria):
        return -self.valor.evaluar(memoria)
    
class NodoAsignacion:
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def evaluar(self, memoria):
        return memoria.declarar(self.nombre, self.valor.evaluar(memoria))
    
class NodoIdentificador:
    def __init__(self, nombre):
        self.nombre = nombre

    def evaluar(self, memoria):
        return memoria.obtener(self.nombre)

class ExepcionReturn(Exception):
    def __init__(self, expresion):
        self.expresion = expresion

class NodoReturn:
    def __init__(self, expresion):
        self.expresion = expresion

    def evaluar(self, memoria):
        valor = self.expresion.evaluar(memoria) if self.expresion else None
        raise ExepcionReturn(valor)
    
class NodoFuncion:
    def __init__(self, nombre, argumentos, cuerpo):
        self.nombre = nombre
        self.argumentos = argumentos
        self.cuerpo = cuerpo

    def evaluar(self, memoria):
        memoria.declarar_funcion(self.nombre, self.argumentos, self.cuerpo)

class NodoLlamada:
    def __init__(self, nombre, argumentos):
        self.nombre = nombre
        self.argumentos = argumentos

    def evaluar(self, memoria):
        func = memoria.llamar_funcion(self.nombre)
        param_nombres = func["argumentos"]
        cuerpo_codigo = func["cuerpo"]

        valores = [arg.evaluar(memoria) for arg in self.argumentos]

        entorno_local = memoria.crear_entorno_local()
        
        for param, valor in zip(param_nombres, valores):
            entorno_local.declarar(param.nombre, valor)

        resultado = None
        
        try:
            for instruccion in cuerpo_codigo:
                resultado = instruccion.evaluar(entorno_local)
        except ExepcionReturn as ret:
            return ret
        
        return resultado           