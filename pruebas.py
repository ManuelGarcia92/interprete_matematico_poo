espacio_variables = {}
variables = ":x=2;:y=7"
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
print(espacio_variables)
            
