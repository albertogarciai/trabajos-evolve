import csv

def calcular_promedio_asignatura(lista_estudiantes, asignatura):
    """
    Calcula el promedio de una asignatura específica
    
    Args:
        lista_estudiantes (list): Lista de diccionarios con datos de estudiantes
        asignatura (str): Nombre de la asignatura
    
    Returns:
        float: Promedio de la asignatura
    """
    if not lista_estudiantes:
        return 0.0
    
    suma_notas = sum(float(estudiante[asignatura]) for estudiante in lista_estudiantes)
    promedio = suma_notas / len(lista_estudiantes)
    return round(promedio, 2)

def calcular_promedio_general(lista_estudiantes):
    """
    Calcula el promedio general de todas las asignaturas
    
    Args:
        lista_estudiantes (list): Lista de diccionarios con datos de estudiantes
    
    Returns:
        float: Promedio general
    """
    if not lista_estudiantes:
        return 0.0
    
    asignaturas = ['matematicas', 'ciencias', 'literatura']
    suma_total = 0
    for estudiante in lista_estudiantes:
        suma_estudiante = sum(float(estudiante[asig]) for asig in asignaturas)
        suma_total += suma_estudiante / len(asignaturas)
    
    return round(suma_total / len(lista_estudiantes), 2)

def leer_notas(nombre_archivo):
    """
    Lee las notas desde un archivo CSV
    
    Args:
        nombre_archivo (str): Ruta del archivo CSV
    
    Returns:
        list: Lista de diccionarios con las notas
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lector_csv = csv.DictReader(archivo)
            return list(lector_csv)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {nombre_archivo}")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {str(e)}")
        return []

# Ejemplo de uso
if __name__ == "__main__":
    estudiantes = leer_notas('notas.csv')
    if estudiantes:
        print("\nListado de estudiantes y sus notas:")
        print("-" * 50)
        for estudiante in estudiantes:
            print(f"{estudiante['nombre']}:")
            print(f"  Matemáticas: {estudiante['matematicas']}")
            print(f"  Ciencias: {estudiante['ciencias']}")
            print(f"  Literatura: {estudiante['literatura']}")
            print("-" * 25)
        
        print("\nPromedios por asignatura:")
        print("-" * 25)
        print(f"Matemáticas: {calcular_promedio_asignatura(estudiantes, 'matematicas')}")
        print(f"Ciencias: {calcular_promedio_asignatura(estudiantes, 'ciencias')}")
        print(f"Literatura: {calcular_promedio_asignatura(estudiantes, 'literatura')}")
        
        print("\nPromedio general del curso:")
        print("-" * 25)
        print(f"Promedio: {calcular_promedio_general(estudiantes)}") 