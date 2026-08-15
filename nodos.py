class Nodo:
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

class NodoBinario(Nodo):
    def __init__(self, operador):
        self.operador = operador
        self.OPERACIONES = {
        "//": lambda x, y: x // y,
        "*" : lambda x, y: x * y,
        "/" : lambda x, y: x / y,
        "+" : lambda x, y: x + y,
        "-" : lambda x, y: x - y,
        }

    def evaluar(self):
        return self.OPERACIONES[self.operador](self.izquierda.evaluar(), self.derecha.evaluar())
    
class NodoSuma(Nodo):
    def evaluar(self):
        return self.izquierda.evaluar() + self.derecha.evaluar()

class NodoResta(Nodo):
    def evaluar(self):
        return self.izquierda.evaluar() - self.derecha.evaluar()
    
class NodoMulti(Nodo):
    def evaluar(self):
        return self.izquierda.evaluar() * self.derecha.evaluar()
    
class NodoDivi(Nodo):
    def evaluar(self):
        return self.izquierda.evaluar() / self.derecha.evaluar()
    
class NodoDiviEntera(Nodo):
    def evaluar(self):
        return self.izquierda.evaluar() // self.derecha.evaluar()

class NodoPotencia(Nodo):
    def evaluar(self):
        return self.izquierda.evaluar() ** self.derecha.evaluar()

class NodoNumero:
    def __init__(self, valor):
        self.valor = valor

    def evaluar(self):
        if "." in self.valor:
            return float(self.valor)
        return int(self.valor)