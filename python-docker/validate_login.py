import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def verificar_credenciais(email, senha):
    try:
        # Conectar ao banco de dados
        mydb = mysql.connector.connect(
            host="mysqldb",
            user="root",
            password="p@ssw0rd1",
            database="tcc"
        )
        cursor = mydb.cursor()

        # Consultar o banco de dados para verificar se o usuário com o email e senha fornecidos existe
        query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
        user_data = (email, senha)
        cursor.execute(query, user_data)
        usuario = cursor.fetchone()  # Retorna uma tupla representando a primeira linha encontrada

        cursor.close()
        mydb.close()

        return usuario  # Retorna o usuário encontrado ou None se não houver correspondência

    except Exception as e:
        print("Error:", e)
        raise e

# @app.route('/', methods=['POST'])
# def login():
#     try:
#         email = request.form['email']
#         senha = request.form['senha']

#         usuario = verificar_credenciais(email, senha)

#         if usuario:
#             # Usuário existe, redirecionar para a página de sucesso ou fazer o que for necessário
#             return redirect(url_for('pagina_de_sucesso'))
#         else:
#             # Usuário não existe, renderizar o template de login novamente com uma mensagem de erro
#             return render_template('/auth/login.html', error='Credenciais inválidas. Tente novamente.')

#     except Exception as e:
#         print("Error:", e)
#         raise e

@app.route('/registros')
def pagina_de_sucesso():
    return "Login bem-sucedido! Você será redirecionado para a página de sucesso."

if __name__ == '__main__':
    app.run(debug=True)
