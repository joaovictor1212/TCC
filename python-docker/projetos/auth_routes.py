from flask import Flask, Blueprint, render_template, request, redirect, url_for
from app import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def login():
    return render_template('/auth/login.html')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            insert_query = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
            user_data = (nome, email, senha)
            cursor.execute(insert_query, user_data)
            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for('auth.login'))

        except Exception as e:
            print("Error:", e)

    return render_template('/auth/cadastro.html')

@auth_bp.route('/recuperar')
def recuperar():
    return render_template('/auth/recuperar.html')
