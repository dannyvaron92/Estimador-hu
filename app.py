from flask import Flask, request, render_template
from recomendador import generar_recomendacion
from obtener_historia_pivote import obtener_historia_pivote

app = Flask(__name__)
DB_PATH = "hu_evaluations.db"

# Crear base de datos si no existe
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            tecnica INTEGER,
            desarrollo INTEGER,
            dependencias INTEGER,
            claridad INTEGER,
            riesgos INTEGER,
            total INTEGER,
            fibonacci INTEGER,
            recomendacion TEXT,
            fecha TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Escala Fibonacci
fibonacci_scale = [0, 1, 2, 3, 5, 8, 13, 21]

def redondear_fibonacci(valor):
    return min(fibonacci_scale, key=lambda x: abs(x - valor))

def obtener_recomendacion(fib_valor):
    if fib_valor <= 8:
        return "✅ Historia aceptable."
    elif fib_valor > 8 and fib_valor < 13:
        return "⚠️ Considera dividir o refinar la historia."
    else:
        return "❌ División recomendada."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        tecnica = int(request.form['tecnica'])
        desarrollo = int(request.form['desarrollo'])
        dependencias = int(request.form['dependencias'])
        claridad = int(request.form['claridad'])
        riesgos = int(request.form['riesgos'])

        
        claridad_transformada = (claridad - 3) * -1
        total = tecnica + desarrollo + dependencias + claridad_transformada + riesgos

        fib_valor = redondear_fibonacci(total)
        recomendacion = obtener_recomendacion(fib_valor)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO evaluations (description, tecnica, desarrollo, dependencias, claridad, riesgos, total, fibonacci, recomendacion, fecha)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (descripcion, tecnica, desarrollo, dependencias, claridad, riesgos, total, fib_valor, recomendacion, fecha))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM evaluations ORDER BY fecha DESC')
    historial = cursor.fetchall()
    conn.close()
    return render_template('index.html', historial=historial)

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
    app.run(host='0.0.0.0', port=10000)
