import numpy as np

# Funzione di interpolazione lineare
def lerp(a, b, t):
    return a + t * (b - a)

# Funzione gradiente
def gradient(h, x, y):
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[0] * x + g[1] * y

# Funzione per la creazione del Perlin Noise in un singolo punto (x, y)
def perlin_noise(x, y, scale=10):
    # Coordinate della griglia
    x0 = int(x // scale) * scale
    y0 = int(y // scale) * scale
    x1 = x0 + scale
    y1 = y0 + scale
    # Coordinate relative all'interno della cella della griglia
    sx = (x - x0) / scale
    sy = (y - y0) / scale
    # Gradiente casuale (usiamo un hash per generare numeri casuali coerenti)
    np.random.seed(x0 + y0 * 57)
    grad00 = np.random.randint(0, 4)
    np.random.seed(x1 + y0 * 57)
    grad10 = np.random.randint(0, 4)
    np.random.seed(x0 + y1 * 57)
    grad01 = np.random.randint(0, 4)
    np.random.seed(x1 + y1 * 57)
    grad11 = np.random.randint(0, 4)
    # Calcolo del prodotto scalare dei vettori gradiente e delle coordinate relative
    n00 = gradient(grad00, x - x0, y - y0)
    n10 = gradient(grad10, x - x1, y - y0)
    n01 = gradient(grad01, x - x0, y - y1)
    n11 = gradient(grad11, x - x1, y - y1)
    # Interpolazione bilineare usando una curva di fade per ottenere transizioni morbide
    u = sx * sx * (3 - 2 * sx)
    v = sy * sy * (3 - 2 * sy)
    nx0 = lerp(n00, n10, u)
    nx1 = lerp(n01, n11, u)
    return lerp(nx0, nx1, v)
