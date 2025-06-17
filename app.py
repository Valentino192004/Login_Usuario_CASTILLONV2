from flask import Flask, request, jsonify, render_template
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite conexión CORS para el fetch

# Configuración de conexión a SQL Server
server = '26.174.243.172'
database = 'CASTILLONV2'
username = 'Ricardo'
password = 'ricardo'
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Ruta raíz para servir el HTML
@app.route('/')
def index():
    return render_template('login.html')

# Función para validar usuario
def validar_usuario(usuario, clave):
    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            query = """
                SELECT * FROM USUARIO
                WHERE LOGEO = ? AND CLAVE = ?
            """
            cursor.execute(query, (usuario, clave))
            row = cursor.fetchone()
            return row is not None
    except Exception as e:
        print("Error al validar usuario:", e)
        return False

# Ruta de login que recibe el fetch del HTML
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('usuario')
    clave = data.get('password')

    if validar_usuario(usuario, clave):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
