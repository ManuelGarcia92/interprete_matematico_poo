import logica
import lexer 
import parser
while True:
    variables = input("Introduce las variables >>> : ").strip()
    operacion = input("Operación >>> : ").strip()
    lista_tokens = lexer.lexer(variables, operacion)
    memoria = logica.crear_tabla_simbolos(variables)
    operacion = parser.parser(memoria, operacion)
    expresion = logica.shuting_yard(operacion, logica.prioridad, logica.asociatividad)
    resultado = logica.evaluar_posfijo(expresion, logica.OPERACIONES)
    print(resultado)
