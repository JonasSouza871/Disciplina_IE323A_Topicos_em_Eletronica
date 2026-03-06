import math


def calcular_afim(x, params):
    """f(x) = a*x + b"""
    a, b = params[0], params[1]
    return a * x + b

def calcular_quadratica(x, params):
    """f(x) = a*x^2 + b*x + c"""
    a, b, c = params[0], params[1], params[2]
    return a * x * x + b * x + c

def calcular_senoidal(x, params):
    """f(x) = a + b * sin(c*x + d)"""
    a, b, c, d = params[0], params[1], params[2], params[3]
    return a + b * math.sin(c * x + d)

def calcular_cossenoidal(x, params):
    """f(x) = a + b * cos(c*x + d)"""
    a, b, c, d = params[0], params[1], params[2], params[3]
    return a + b * math.cos(c * x + d)

def calcular_vertice_delta(params):
    """Calcula Xv, Yv e Delta para funcao quadratica (ax^2 + bx + c)."""
    a, b, c = params[0], params[1], params[2]
    if a == 0:
        return 0.0, 0.0, 0.0
    delta = b * b - 4 * a * c
    xv = -b / (2 * a)
    yv = -delta / (4 * a)
    return xv, yv, delta

#Mapa de funcoes indexado pelo tipo
FUNCOES = [
    calcular_afim,
    calcular_quadratica,
    calcular_senoidal,
    calcular_cossenoidal,
]
