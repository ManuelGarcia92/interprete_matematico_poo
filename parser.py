def parser(memoria, operacion):
    e = 0
    tokens_crudos = []
    while e < len(operacion):
        if operacion[e] in memoria:
            tokens_crudos.append(memoria[operacion[e]])
            e += 1
        else:
            tokens_crudos.append(operacion[e])
            e += 1  
    return tokens_crudos