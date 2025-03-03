# calculadora.py
import sys

def multiplicar_por_diez(numero):
    """Multiplica un número por 10.

    Args:
        numero (int): El número a multiplicar.

    Returns:
        int: El resultado de la multiplicación.
    """
    return numero * 10

numero = int(input("Ingrese un número: "))
resultado = multiplicar_por_diez(numero)
print(f"El resultado de multiplicar {numero} por 10 es: {resultado}")