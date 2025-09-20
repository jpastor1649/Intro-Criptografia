import numpy as np
from math import gcd
from sympy import Matrix  # más preciso para determinantes enteros


def generate_key(n: int) -> np.ndarray:
    """Generate a random invertible key matrix of size n x n (mod 26)."""
    while True:
        key = np.random.randint(0, 26, size=(n, n))  # matriz aleatoria
        det = int(Matrix(key).det())
        det_mod = det % 26
        if det_mod != 0 and gcd(det_mod, 26) == 1:
            return key

# ejemplo con 5x5
key = generate_key(5)
print("Generated key 5x5:\n", key)

def validate_key(key: list[list[int]]) -> np.ndarray:
    """Validate that the key is a square matrix and invertible modulo 26."""
    key = np.array(key)
    det = int(Matrix(key).det())  # determinante exacto
    det_mod = det % 26
    if det_mod == 0 or gcd(det_mod, 26) != 1:
        raise ValueError("Key matrix is not invertible modulo 26")
    return key

validate_key(key)  # debería pasar sin errores
