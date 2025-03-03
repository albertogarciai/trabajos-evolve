def pertenece_a_fibonacci(numero):
    """Determina si un número pertenece a la serie de Fibonacci.

    Args:
        numero (int): Número a verificar.

    Returns:
        bool: True si el número pertenece a la serie, False si no.
    """
    a, b = 0, 1
    while b < numero:
        a, b = b, a + b
    return b == numero

numero = int(input("Ingrese un número: "))
if pertenece_a_fibonacci(numero):
    print(f"El número {numero} pertenece a la serie de Fibonacci.")
else:
    print(f"El número {numero} no pertenece a la serie de Fibonacci.")
