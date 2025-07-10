#!/usr/bin/env python3
from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import hashlib
import os

app = Flask(__name__)
DATABASE = 'auth.db'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Autenticación</title>
</head>
<body>
    <h2>{{ message }}</h2>
    <form method="POST">
        Usuario: <input type="text" name="username"><br>
        Contraseña: <input type="password" name="password"><br>
        <input type="submit" value="Ingresar">
    </form>
</body>
</html>
"""

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                      (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        stored_hash = result[0]
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        return input_hash == stored_hash
    return False

@app.route('/', methods=['GET', 'POST'])
def login():
    message = "Ingrese sus credenciales"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if verify_user(username, password):
            message = f"¡Bienvenido {username}!"
        else:
            message = "Credenciales inválidas. Intente nuevamente."
    
    return render_template_string(HTML_TEMPLATE, message=message)

def main():
    init_db()
    create_user("Juan", "123")
    create_user("Damaso", "456")
    print(f"Servidor iniciado en http://localhost:7500")
    app.run(host='0.0.0.0', port=7500, debug=True)

if __name__ == '__main__':
    main()