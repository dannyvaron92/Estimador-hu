from typing import Dict, Tuple

# Lista de números Fibonacci relevantes para estimación ágil
FIBONACCI_SERIE = [1, 2, 3, 5, 8, 13, 21, 34]

def transformar_claridad(valor: int) -> int:
    """Aplica la fórmula especial para claridad de requisitos."""
    return (valor - 3) * -1

def aproximar_fibonacci(valor: int) -> int:
    """Aproxima el valor al número Fibonacci más cercano."""
    diferencias = {fib: abs(fib - valor) for fib in FIBONACCI_SERIE}
    return min(diferencias, key=diferencias.get)

def calcular_puntaje_total(criterios: Dict[str, int]) -> int:
    """Calcula la suma total de criterios con fórmula especial para claridad."""
    total = (
        criterios.get("complejidad_tecnica", 0) +
        criterios.get("esfuerzo_desarrollo", 0) +
        criterios.get("dependencias_externas", 0) +
        transformar_claridad(criterios.get("claridad_requisitos", 0)) +
        criterios.get("riesgos_incertidumbre", 0)
    )
    return total

def generar_recomendacion(hu: str, criterios: Dict[str, int], criterios_pivote: Dict[str, int], hu_pivote: str) -> Tuple[int, str]:
    """
    Calcula el puntaje Fibonacci sugerido y genera una recomendación textual.
    """
    total_actual = calcular_puntaje_total(criterios)
    total_pivote = calcular_puntaje_total(criterios_pivote)

    puntaje_sugerido = aproximar_fibonacci(total_actual)

    diferencia = total_actual - total_pivote
    if diferencia > 0:
        mensaje = f"La historia '{hu}' parece más compleja que la historia pivote '{hu_pivote}' en base a los criterios ingresados."
    elif diferencia < 0:
        mensaje = f"La historia '{hu}' parece menos compleja que la historia pivote '{hu_pivote}'."
    else:
        mensaje = f"La historia '{hu}' tiene una complejidad similar a la historia pivote '{hu_pivote}'."

    return puntaje_sugerido, mensaje
