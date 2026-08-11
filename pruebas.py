OPERACIONES = {
    "**": lambda x, y: x ** y,
    "$" : lambda x, y: x ** (1 / y),
    "*" : lambda x, y: x * y,
    "/" : lambda x, y: x / y,
    "//": lambda x, y: x // y,
    "+" : lambda x, y: x + y,
    "-" : lambda x, y: x - y
}

prioridad = {"+":1,"-":1,"*":2,"/":2,"**":3}

asociatividad = {"+":"L","-":"L","*":"L","/":"L","**":"R"}

def shuting_yard(tokens, prioridad, asociatividad):
    cola_salida = []
    pila_operadores = []
    for token in tokens:
        if token.replace(".","", 1).isdigit() or (token.startswith("-") and len(token) > 1):
            cola_salida.append(token)
        elif token == "(":
            pila_operadores.append(token)
        elif token == ")":
            while pila_operadores and pila_operadores[-1] != "(":
                cola_salida.append(pila_operadores.pop())   
            if pila_operadores:
                pila_operadores.pop()         
        elif token in prioridad:
            while (pila_operadores and pila_operadores[-1] != "(" and
                    (prioridad[pila_operadores[-1]] > prioridad[token] or 
                     (prioridad[pila_operadores[-1]] == prioridad[token] and asociatividad[token] == "L"))):
                cola_salida.append(pila_operadores.pop())
            pila_operadores.append(token)
    while pila_operadores:
        cola_salida.append(pila_operadores.pop())
    return cola_salida

def evaluar_posfijo(lista_posfijo, operaciones):
    pila_numeros = []
    for token in lista_posfijo:
        if token in operaciones:
            b = float(pila_numeros.pop())
            a = float(pila_numeros.pop())
            resultado = operaciones[token](a, b)
            pila_numeros.append(resultado)
        else:
            pila_numeros.append(token)
    return pila_numeros[0] if pila_numeros else 0

espacio_variables = {}
variables = input("Introduce las variables >>> : ").strip()
operacion = input("Operación >>> : ").strip()
buffer_nombre = ""
buffer_valor = ""
i = 0
while i < len(variables):
    if variables[i] == ":":
        i += 1
        while i < len(variables) and variables[i] != "=":
            buffer_nombre += variables[i]
            i += 1
    if i < len(variables) and variables[i] == "=":
        i += 1
        while i < len(variables) and variables[i] != ";":
            buffer_valor += variables[i]
            i += 1
    espacio_variables[buffer_nombre] = buffer_valor
    buffer_nombre = "" ; buffer_valor = ""
    i += 1
e = 0
tokens_crudos = []
while e < len(operacion):
    if operacion[e] in espacio_variables:
        tokens_crudos.append(espacio_variables[operacion[e]])
        e += 1
    else:
        tokens_crudos.append(operacion[e])
        e += 1  
        
expresion = shuting_yard(tokens_crudos, prioridad, asociatividad)
resultado = evaluar_posfijo(expresion, OPERACIONES)
print(resultado)