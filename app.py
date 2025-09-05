from flask import Flask, request, render_template
from recomendador import generar_recomendacion
from obtener_historia_pivote import obtener_historia_pivote

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
    app.run(debug=True)
