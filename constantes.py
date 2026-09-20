import operaciones 
OPERACIONES = {
    "**": lambda x, y: x ** y,
    "$" : lambda x, y: operaciones.raiz_enesima(x, y),
    "//": lambda x, y: operaciones.division_entera(x, y),
    "%" : lambda x, y: operaciones.modulo(x, y),
    "/" : lambda x, y: operaciones.division(x, y),
    "*" : lambda x, y: x * y,
    "-" : lambda x, y: x - y,
    "+" : lambda x, y: x + y
} 

PALABRAS_RESERVADAS = {
    "def"    : "DEF",
    "return" : "RETURN",
}

OPERADORES_SIMPLES = {
    "+"  : "SUMA",
    "-"  : "RESTA",
    "*"  : "MULTI",
    "/"  : "DIV",
    "$"  : "RAIZ_ENESIMA",
    "%"  : "MOD",
    "("  : "PAREN_IZQ",
    ")"  : "PAREN_DER",
    "{"  : "LLAVE_IZQ",
    "}"  : "LLAVE_DER",
    "="  : "ASIGNACION",
    ","  : "COMA",
    ";"  : "PUNTO_Y_COMA",
}

OPERADORES_DOBLES = {
    "**" : "POTENCIA",
    "//" : "DIV_ENTERA",
}