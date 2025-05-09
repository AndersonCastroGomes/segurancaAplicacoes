from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def buscar_usuario(matricula, senha):
    con = sqlite3.connect('biblioteca.db')
    cursor = con.cursor()
    
    # Consulta vulnerável a SQL Injection
    query = f"SELECT * FROM usuarios WHERE matricula = '{matricula}' AND senha = '{senha}'"
    
    try:
        cursor.execute(query)
        return cursor.fetchone()
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        con.close()

def buscar_livros(titulo):
    con = sqlite3.connect('biblioteca.db')
    cursor = con.cursor()
    
    # Consulta vulnerável a SQL Injection
    query = f"SELECT * FROM livros WHERE titulo LIKE '%{titulo}%'"
    
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        con.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    mensagem = ''
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        usuario = buscar_usuario(matricula, senha)
        
        if usuario:
            return redirect(url_for('buscar', user_id=usuario[0]))
        else:
            mensagem = "Matrícula ou senha inválidos."
    
    return render_template('login.html', mensagem=mensagem)

@app.route('/buscar/<int:user_id>', methods=['GET', 'POST'])
def buscar(user_id):
    livros = None
    if request.method == 'POST':
        titulo = request.form['titulo']
        livros = buscar_livros(titulo)
    
    return render_template('buscar.html', livros=livros)

if __name__ == '__main__':
    app.run(debug=True)