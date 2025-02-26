from fastapi import FastAPI

app = FastAPI()

@app.get("/sumar/{num1}/{num2}")
def sumar(num1: float, num2: float):
    """Suma dos números.

    Args:
        num1 (float): Primer número.
        num2 (float): Segundo número.

    Returns:
        float: Suma de los dos números.
    """
    return {"resultado": num1 + num2}

@app.get("/restar/{num1}/{num2}")
def restar(num1: float, num2: float):
    """Resta dos números.

    Args:
        num1 (float): Primer número.
        num2 (float): Segundo número.

    Returns:
        float: Resta de los dos números.
    """
    return {"resultado": num1 - num2}

@app.get("/multiplicar/{num1}/{num2}")
def multiplicar(num1: float, num2: float):
    """Multiplica dos números.

    Args:
        num1 (float): Primer número.
        num2 (float): Segundo número.

    Returns:
        float: Multiplicación de los dos números.
    """
    return {"resultado": num1 * num2}

@app.get("/dividir/{num1}/{num2}")
def dividir(num1: float, num2: float):
    """Divide dos números.

    Args:
        num1 (float): Primer número.
        num2 (float): Segundo número.

    Returns:
        float: División de los dos números.
    """
    if num2 == 0:
        return {"error": "No se puede dividir por cero"}
    return {"resultado": num1 / num2}
