from flask import Blueprint, render_template, request, redirect, url_for, Flask
from app import get_db_connection

registros_bp = Blueprint('registros', __name__)

@registros_bp.route('/', methods=['GET', 'POST'])
def registros():
    if request.method == 'POST':
        arquivo = request.files['arquivo'].read()
        coordenada_x = request.form['coordenada_x']
        coordenada_y = request.form['coordenada_y']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            insert_query = "INSERT INTO registros (arquivo, coordenada_x, coordenada_y) VALUES (%s, %s, %s)"
            user_data = (arquivo, coordenada_x, coordenada_y)
            cursor.execute(insert_query, user_data)
            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for('registros.registros'))

        except Exception as e:
            print("Error:", e)

    return render_template('/principal/registros.html')
