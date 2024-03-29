import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, jsonify, json
import base64


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
    

# @app.route('/lista-registros')
# def lista_registros():
#     resposta = trazer_registros()
#     print(resposta)
    # result = json.dumps(resposta)
    # if result:
    #     try:
    #         return render_template('/principal/lista-registros.html', registros=result)
    #     except Exception as e:
    #         print("Error:", e)
    #         raise e




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