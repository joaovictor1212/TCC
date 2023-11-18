import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, jsonify, json, Response
import base64
import os
import pdb


app = Flask(__name__)


class MySqlBd():
    def conectar_bd():
        return mysql.connector.connect(
            host="mysqldb",
            user="root",
            password="p@ssw0rd1",
            database="tcc",
        )



class Login():
    
    
    @app.route('/')
    @app.route('/login', methods=['GET','POST'])
    def login():
        
        if request.method == 'POST':
            username = request.form['email']
            password = request.form['senha']
            print(username, password)
            valida  = Login.validar_login(username=username, password=password)
            if valida:
                print(valida)
                # Login bem-sucedido, redirecionar para a página principal ou realizar outras ações necessárias
                # session['username'] = username  # Salvar o nome de usuário na sessão, se necessário
                return redirect(url_for('registros'))
            else:
                error_message = "Usuário ou senha incorretos. Tente novamente."
                return render_template('/auth/login.html', error_message=error_message)
            
        return render_template('/auth/login.html')

    
    def validar_login(username, password):
        # Esta função valida o login no banco de dados
        # Retorna True se as credenciais estiverem corretas, False caso contrário

        mydb =  MySqlBd.conectar_bd()

        cursor = mydb.cursor()

        query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()

        cursor.close()
        mydb.close()

        return usuario is not None
        
    
    
    @app.route('/recuperar', methods=['GET','POST'])
    def recuperar():
        if request.method == 'POST':
            username = request.form['email']
            senha = Login.get_password(username=username)
            print(senha)
            if senha:
                message = "Sua senha é: %s" %senha
            return render_template('/auth/recuperar.html', message=message)
        else:
            return render_template('/auth/recuperar.html')

    
    def get_password(username):
        mydb =  MySqlBd.conectar_bd()
        cursor = mydb.cursor()
        print(username)
        query = "SELECT u.senha FROM usuarios u WHERE email = %s"
        cursor.execute(query, (username,))
        senha = cursor.fetchone()
        
        cursor.close()
        mydb.close()

        return senha[0] if senha else None
    

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        try:
            Login.cadastro_usuario()
            if request.method == 'POST':
                # Get user data from the form
                nome = request.form['nome']
                email = request.form['email']
                senha = request.form['senha']

                # Connect to the MySQL database
                mydb = MySqlBd.conectar_bd()
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


    @app.route('/initdb', methods=['GET','POST'])
    def cadastro_usuario():

        # Após criar o banco de dados, você precisa se conectar novamente para usá-lo
        mydb =  MySqlBd.conectar_bd()
        cursor = mydb.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (  id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, senha VARCHAR(255) NOT NULL);")

        cursor.close()
        mydb.close()

        return 'init database'



class Registros():
    
    
    @app.route('/registros', methods=['GET','POST'])
    def registros():
        try:
            Registros.cadastro_registros()
            if request.method == 'POST':
                arquivo = request.files['arquivo'].read()
                coordenada_x = request.form['coordenada_x']
                coordenada_y = request.form['coordenada_y']

                # Connect to the MySQL database
                mydb = MySqlBd.conectar_bd()
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
        
        
    @app.route('/initdb', methods=['GET','POST'])
    def cadastro_registros():

        # Após criar o banco de dados, você precisa se conectar novamente para usá-lo
        mydb =  MySqlBd.conectar_bd()
        cursor = mydb.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS registros (  id INT AUTO_INCREMENT PRIMARY KEY, arquivo LONGBLOB, coordenada_x DECIMAL(10, 4) NOT NULL, coordenada_y DECIMAL(10, 4) NOT NULL);")

        cursor.close()
        mydb.close()

        return 'init database'


    @app.route('/api/registros', methods=['GET'])
    def trazer_registros():
        print("Verificando acesso a rota")
        if request.method == 'GET':
        # Connect to the MySQL database
            mydb =  MySqlBd.conectar_bd()
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
        resposta = Registros.trazer_registros()

        # Verificar se a resposta é um objeto de resposta Flask
        if isinstance(resposta, Response):
            # Se for, extrair os dados do conteúdo da resposta
            registros = resposta.get_json()# Use o método adequado para extrair os dados
        else:
            # Se não for, assumir que a resposta já contém os dados necessários
            registros = resposta
            
        try:
            for registro in registros:
                registro_id = registro['id']
                Registros.editar_registro(registro_id=registro_id)
                Registros.excluir_registro(registro_id=registro_id)

            return render_template('/principal/lista-registros.html', registros=registros)
        except Exception as e:
            print("Error:", e)
            raise e
    
    
    
    
    @app.route('/editar-registro/<int:registro_id>', methods=['GET','POST'])
    def editar_registro(registro_id):
        registros = []
         
        if request.method == 'GET':
            if registro_id:
                registro = Registros.obter_registro(registro_id=registro_id)
                return render_template('/principal/editar-registro.html', registro=registro)
        
        
        elif request.method == 'POST':
            resposta = Registros.trazer_registros()
            
            novo_arquivo = request.files['novoArquivo']
            # Verificar se um novo arquivo foi enviado
            if novo_arquivo:
                arquivo = novo_arquivo.read()
            else:
                # Se nenhum novo arquivo foi enviado, manter o arquivo anterior
                registro_atual = Registros.obter_registro(registro_id=registro_id)
                arquivo = registro_atual['arquivo']
                
            coordenada_x = request.form['novaCoordenadaX']
            coordenada_y = request.form['novaCoordenadaY']

        
            # Atualize o registro
            Registros.atualizar_registro(registro_id=registro_id, arquivo=arquivo, coordenada_x=coordenada_x, coordenada_y=coordenada_y)

            # Renderizar o modelo com o registro atualizado
            if isinstance(resposta, Response):
            # Se for, extrair os dados do conteúdo da resposta
                registros = resposta.get_json()
            return redirect(url_for('lista_registros'))
    
    
    def obter_registro(registro_id):
        mydb =  MySqlBd.conectar_bd()
        cursor = mydb.cursor()

        # Usando placeholders para evitar injeção de SQL
        query = "SELECT * FROM registros WHERE id = %s"
        cursor.execute(query, (registro_id,))
        data = cursor.fetchall()

        cursor.close()
        mydb.close()

        if data:
            for value in data:
                registro = {
                    'id': value[0],
                    'arquivo': value[1],
                    'coordenada_x': value[2],
                    'coordenada_y': value[3]
                }
            return registro
        return None
    
    
    def atualizar_registro(registro_id, arquivo, coordenada_x, coordenada_y):
        mydb =  MySqlBd.conectar_bd()
        cursor = mydb.cursor()
        
        # coordenada_x = int(coordenada_x)
        # coordenada_y = int(coordenada_y)
        
        query = "UPDATE registros SET arquivo = %s, coordenada_x = %s, coordenada_y = %s WHERE id = %s"
        cursor.execute(query, (arquivo, coordenada_x, coordenada_y, int(registro_id)))
        
        mydb.commit()
        cursor.close()
        mydb.close()
    
    
        
    @app.route('/excluir-registro/<int:registro_id>', methods=['POST'])
    def excluir_registro(registro_id):
        # Verifica se o método da requisição é POST
        if request.method == 'POST':
            # Após criar o banco de dados, você precisa se conectar novamente para usá-lo
            if registro_id:
                mydb =  MySqlBd.conectar_bd()
                cursor = mydb.cursor()

                # Usando placeholders para evitar injeção de SQL
                query = "DELETE FROM registros WHERE id = %s"
                cursor.execute(query, (registro_id,))

                mydb.commit()
                cursor.close()
                mydb.close()
                print("Registro excluído com sucesso!")

        return redirect(url_for('lista_registros'))





  
       
       

    


# Rota para excluir um registro específico











if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)