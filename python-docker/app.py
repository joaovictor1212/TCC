import mysql.connector
import json
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def login():
    try:
        return render_template('auth.html')
    except Exception as e:
        print("Error:", e)
        raise e
    
@app.route('/cadastro')
def cadastro():
    try:
        return render_template('cadastro.html')
    except Exception as e:
        print("Error:", e)
        raise e



@app.route('/widgets')
def get_widgets():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()


    cursor.execute("SELECT * FROM widgets")

    row_headers=[x[0] for x in cursor.description] #this will extract row headers

    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()

    return json.dumps(json_data)

@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.execute("USE inventory")

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    return 'init database'

if __name__ == "__main__":
    app.run(host ='0.0.0.0')