from flask import Flask, request, render_template
from recomendador import generar_recomendacion
from obtener_historia_pivote import obtener_historia_pivote

import os


import sqlite3
from datetime import datetime

# Guardar en historial_evaluaciones
try:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historial_evaluaciones (
            texto,
            complejidad_tecnica,
            esfuerzo_desarrollo,
            dependencias_externas,
            claridad_requisitos,
            riesgos_incertidumbre,
            puntaje_sugerido,
            recomendacion,
            fecha_evaluacion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        hu_texto,
        criterios["complejidad_tecnica"],
        criterios["esfuerzo_desarrollo"],
        criterios["dependencias_externas"],
        criterios["claridad_requisitos"],
        criterios["riesgos_incertidumbre"],
        puntaje_sugerido,
        mensaje,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()
except Exception as e:
    return f"Error al guardar en historial: {e}", 500


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/evaluar', methods=['POST'])
def evaluar_historia():
    hu_texto = request.form['hu']
    criterios = {
        "complejidad_tecnica": int(request.form['complejidad_tecnica']),
        "esfuerzo_desarrollo": int(request.form['esfuerzo_desarrollo']),
        "dependencias_externas": int(request.form['dependencias_externas']),
        "claridad_requisitos": int(request.form['claridad_requisitos']),
        "riesgos_incertidumbre": int(request.form['riesgos_incertidumbre']),
    }

    pivote = obtener_historia_pivote()
    if not pivote:
        return "No se encontró historia pivote", 400

    puntaje_sugerido, mensaje = generar_recomendacion(
        hu=hu_texto,
        criterios=criterios,
        criterios_pivote=pivote['criterios'],
        hu_pivote=pivote['texto']
    )

    return render_template('resultado.html', puntaje=puntaje_sugerido, mensaje=mensaje)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render asigna el puerto en PORT
    app.run(host='0.0.0.0', port=port)
