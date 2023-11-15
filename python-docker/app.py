import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, jsonify, json, Response
import base64
import os


app = Flask(__name__)


@app.route('/')
def login():
    try:
        return render_template('/auth/login.html')
    except Exception as e:
        print("Error:", e)
        raise e

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    try:
        cadastro_usuario()
        if request.method == 'POST':
            # Get user data from the form
            nome = request.form['nome']
            email = request.form['email']
            senha = request.form['senha']

            # Connect to the MySQL database
            mydb = mysql.connector.connect(
                host="mysqldb",
                user="root",
                password="p@ssw0rd1",
                database="tcc"
            )
            cursor = mydb.cursor()

            # Insert user data into the usuarios table
            insert_query = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
            user_data = (nome, email, senha)
            cursor.execute(insert_query, user_data)
            mydb.commit()

            cursor.close()
            mydb.close()

            return redirect(url_for('login'))  # Redirect to the login page after successful registration

        return render_template('/auth/cadastro.html')  # Render the registration form for GET requests

    except Exception as e:
        print("Error:", e)
        raise e

@app.route('/recuperar')
def recuperar():
    try:
        return render_template('/auth/recuperar.html')
    except Exception as e:
        print("Error:", e)
        raise e

@app.route('/registros', methods=['GET','POST'])
def registros():
    try:
        cadastro_registros()
        if request.method == 'POST':
            arquivo = request.files['arquivo'].read()
            coordenada_x = request.form['coordenada_x']
            coordenada_y = request.form['coordenada_y']

             # Connect to the MySQL database
            mydb = mysql.connector.connect(
                host="mysqldb",
                user="root",
                password="p@ssw0rd1",
                database="tcc"
            )
            cursor = mydb.cursor()

            # Insert user data into the usuarios table
            insert_query = "INSERT INTO registros (arquivo, coordenada_x, coordenada_y) VALUES (%s, %s, %s)"
            user_data = (arquivo, coordenada_x, coordenada_y)
            cursor.execute(insert_query, user_data)
            mydb.commit()

            cursor.close()
            mydb.close()

            return redirect(url_for('registros'))

        return render_template('/principal/registros.html')

    except Exception as e:
        print("Error:", e)
        raise e


@app.route('/api/registros', methods=['GET'])
def trazer_registros():
    print("Verificando acesso a rota")
    if request.method == 'GET':
     # Connect to the MySQL database
        mydb = mysql.connector.connect(
            host="mysqldb",
            user="root",
            password="p@ssw0rd1",
            database="tcc"
        )
        cursor = mydb.cursor()
        query = "SELECT * FROM registros"
        cursor.execute(query)
        registros = cursor.fetchall()  # Obtendo todos os registros da consulta
        cursor.close()
        mydb.close()

        # Convertendo registros para um formato serializável (por exemplo, lista de dicionários)
        registros_serializaveis = []
        for registro in registros:
            arquivo_bytes = registro[1]  # Assumindo que o arquivo está no segundo campo da tupla
            arquivo_base64 = base64.b64encode(arquivo_bytes).decode('utf-8')  # Convertendo para base64
            registro_dict = {
                'id': registro[0],
                'arquivo': arquivo_base64,  # Usando a representação base64 do arquivo
                'coordenada_x': registro[2],
                'coordenada_y': registro[3]
                # Adicione mais campos conforme necessário
            }
            registros_serializaveis.append(registro_dict)

        return jsonify(registros_serializaveis)


@app.route('/lista-registros')
def lista_registros():
    resposta = trazer_registros()

    # Verificar se a resposta é um objeto de resposta Flask
    if isinstance(resposta, Response):
        # Se for, extrair os dados do conteúdo da resposta
        registros = resposta.get_json() # Use o método adequado para extrair os dados
        for registro_id in registros:
            editar_registro(registro_id=registro_id)
            excluir_registro(registro_id=registro_id)
    else:
        # Se não for, assumir que a resposta já contém os dados necessários
        registros = resposta

    try:
        return render_template('/principal/lista-registros.html', registros=registros)
    except Exception as e:
        print("Error:", e)
        raise e


@app.route('/editar-registro/<int:registro_id>', methods=['GET', 'POST'])
def editar_registro(registro_id):

    if request.method == 'POST':
        # Após criar o banco de dados, você precisa se conectar novamente para usá-lo
        if registro_id:
            mydb = mysql.connector.connect(
                host="mysqldb",
                user="root",
                password="p@ssw0rd1",
                database="tcc"
            )
            cursor = mydb.cursor()

            # Usando placeholders para evitar injeção de SQL
            query = "SELECT * FROM registros WHERE id = %s"
            cursor.execute(query, (registro_id,))
            data = cursor.fetchall()
            
            cursor.close()
            mydb.close()
            if data:
                print("Registro encontrado com sucesso!")
                return redirect(url_for('lista_registros'))
    


# Rota para excluir um registro específico
@app.route('/excluir-registro/<int:registro_id>', methods=['POST'])
def excluir_registro(registro_id):
    # Verifica se o método da requisição é POST
    if request.method == 'POST':
        # Após criar o banco de dados, você precisa se conectar novamente para usá-lo
        if registro_id:
            mydb = mysql.connector.connect(
                host="mysqldb",
                user="root",
                password="p@ssw0rd1",
                database="tcc"
            )
            cursor = mydb.cursor()

            # Usando placeholders para evitar injeção de SQL
            query = "DELETE FROM registros WHERE id = %s"
            cursor.execute(query, (registro_id,))

            mydb.commit()
            cursor.close()
            mydb.close()
            print("Registro excluído com sucesso!")

    return redirect(url_for('lista_registros'))




@app.route('/initdb', methods=['GET','POST'])
def cadastro_usuario():

    # Após criar o banco de dados, você precisa se conectar novamente para usá-lo
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="tcc"
    )
    cursor = mydb.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (  id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, senha VARCHAR(255) NOT NULL);")


    cursor.close()
    mydb.close()

    return 'init database'


@app.route('/initdb', methods=['GET','POST'])
def cadastro_registros():

    # Após criar o banco de dados, você precisa se conectar novamente para usá-lo
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="tcc"
    )
    cursor = mydb.cursor()


    cursor.execute("CREATE TABLE IF NOT EXISTS registros (  id INT AUTO_INCREMENT PRIMARY KEY, arquivo LONGBLOB, coordenada_x DECIMAL(10, 4) NOT NULL, coordenada_y DECIMAL(10, 4) NOT NULL);")

    cursor.close()
    mydb.close()

    return 'init database'

if __name__ == "__main__":
    app.run(host='0.0.0.0')