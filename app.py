from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Configura la ruta de la base de datos en tu Mac
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventario.db')

def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Esta función crea la tabla automáticamente al iniciar
def inicializar_db():
    conn = conectar_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Capa de Presentación: Muestra la página web con los datos
@app.route('/')
def index():
    conn = conectar_db()
    productos = conn.execute('SELECT * FROM productos ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

# Capa de Lógica: Recibe los datos del formulario y los guarda
@app.route('/agregar', methods=['POST'])
def agregar_producto():
    nombre = request.form.get('nombre')
    cantidad = request.form.get('cantidad')
    
    if nombre and cantidad:
        conn = conectar_db()
        conn.execute('INSERT INTO productos (nombre, cantidad) VALUES (?, ?)', (nombre, cantidad))
        conn.commit()
        conn.close()
        
    return redirect(url_for('index'))
# Capa de Lógica: Eliminar un registro por su ID
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conn = conectar_db()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    inicializar_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
