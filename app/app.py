import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "admin")
DB_DB = os.getenv("POSTGRES_DB", "actividad_db")
DB_HOST = "db"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_DB,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Bienvenido a la API",
        "endpoints": [
            "/users (GET, POST)",
            "/users/<id> (GET, PUT, DELETE)",
            "/products (GET, POST)",
            "/products/<id> (GET, PUT/PATCH, DELETE)"
        ]
    })

# --- RUTAS DE USUARIOS ---
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM users WHERE id = %s;', (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return jsonify(user)
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({"error": "Nombre y correo son obligatorios"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('INSERT INTO users (name, email) VALUES (%s, %s) RETURNING *;', (name, email))
        user = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
    return jsonify(user), 201

@app.route('/users/<int:id>', methods=['PUT', 'PATCH'])
def update_user(id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('UPDATE users SET name = COALESCE(%s, name), email = COALESCE(%s, email) WHERE id = %s RETURNING *;', (name, email, id))
        user = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
        
    if user:
        return jsonify(user)
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('DELETE FROM users WHERE id = %s RETURNING *;', (id,))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    if user:
        return jsonify({"message": "Usuario eliminado correctamente", "user": user})
    return jsonify({"error": "Usuario no encontrado"}), 404

# --- RUTAS DE PRODUCTOS ---
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM products;')
    products = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock', 0)
    
    if not name or price is None:
        return jsonify({"error": "Nombre y precio son obligatorios"}), 400
        
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('INSERT INTO products (name, price, stock) VALUES (%s, %s, %s) RETURNING *;', (name, price, stock))
        product = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
    return jsonify(product), 201

@app.route('/products/<int:id>', methods=['PUT', 'PATCH'])
def update_product(id):
    data = request.json
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('UPDATE products SET name = COALESCE(%s, name), price = COALESCE(%s, price), stock = COALESCE(%s, stock) WHERE id = %s RETURNING *;', (name, price, stock, id))
        product = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
        
    if product:
        return jsonify(product)
    return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('DELETE FROM products WHERE id = %s RETURNING *;', (id,))
    product = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    if product:
        return jsonify({"message": "Producto eliminado correctamente", "product": product})
    return jsonify({"error": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
