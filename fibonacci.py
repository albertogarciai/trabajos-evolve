def fibonacci(n):
    """Genera los primeros n números de la serie de Fibonacci.

    Args:
        n (int): Número de términos de la serie.

    Returns:
        list: Lista con los primeros n números de la serie de Fibonacci.
    """
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        next_number = fib_sequence[-1] + fib_sequence[-2]
        fib_sequence.append(next_number)
    return fib_sequence


n = 10
resultado = fibonacci(n)
print(f"Los primeros {n} números de la serie de Fibonacci son: {resultado}")