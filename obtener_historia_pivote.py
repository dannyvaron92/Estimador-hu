import sqlite3

def obtener_historia_pivote():
    conn = sqlite3.connect('database.db')  # Ajusta el nombre si es diferente
    cursor = conn.cursor()
    
    cursor.execute("SELECT texto, complejidad_tecnica, esfuerzo_desarrollo, dependencias_externas, claridad_requisitos, riesgos_incertidumbre FROM historia_pivote LIMIT 1")
    fila = cursor.fetchone()
    conn.close()

    if fila:
        return {
            'texto': fila[0],
            'criterios': {
                'complejidad_tecnica': fila[1],
                'esfuerzo_desarrollo': fila[2],
                'dependencias_externas': fila[3],
                'claridad_requisitos': fila[4],
                'riesgos_incertidumbre': fila[5]
            }
        }
    else:
        return None
