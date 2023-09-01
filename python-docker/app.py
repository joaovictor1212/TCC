import mysql.connector
import json
from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/registros')
def cadastro_padrao():
    try:
        return render_template('/principal/registros.html')
    except Exception as e:
        print("Error:", e)
        raise e

# @app.route('/users')
# def get_widgets():
#     mydb = mysql.connector.connect(
#         host="mysqldb",
#         user="root",
#         password="p@ssw0rd1",
#         database="tcc"
#     )
#     cursor = mydb.cursor()


#     cursor.execute("SELECT * FROM widgets")

#     row_headers=[x[0] for x in cursor.description] #this will extract row headers

#     results = cursor.fetchall()
#     json_data=[]
#     for result in results:
#         json_data.append(dict(zip(row_headers,result)))

#     cursor.close()

#     return json.dumps(json_data)

@app.route('/initdb')
def db_init():
   
    # Após criar o banco de dados, você precisa se conectar novamente para usá-lo
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="tcc"
    )
    cursor = mydb.cursor()

    cursor.execute("CREATE TABLE usuarios (  id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, senha VARCHAR(255) NOT NULL)")
    
    cursor.execute("CREATE TABLE registros (  id INT AUTO_INCREMENT PRIMARY KEY, arquivo_padrao VARCHAR(255) NOT NULL, coordenada_x DECIMAL(10, 4) NOT NULL, coordenada_y DECIMAL(10, 4) NOT NULL")
    
    cursor.close()
    mydb.close()

    return 'init database'

if __name__ == "__main__":
    app.run(host='0.0.0.0')