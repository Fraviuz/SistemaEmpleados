from colorama import Cursor
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app=Flask(__name__)
mysql= MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='sistema'

mysql.init_app(app)
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

#Pagina index, muestra todos los empleados en la base de dato.
@app.route('/')
def index():  
    sql = "SELECT * FROM `sistema`.`empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit()
    return render_template('empleados/index.html', empleados=empleados)

#Formulario para crear y agregar un empleado.
@app.route('/create')
def create():
    return render_template('empleados/create.html')

#Insertar empleado creado en create a la base de datos.
@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')
    
    if _foto.filename!='':
        nuevo_nombre_foto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevo_nombre_foto)

    sql = 'INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);'
    datos=(_nombre, _correo, nuevo_nombre_foto)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template('empleados/index.html')

#Remueve empleado desde el index.
@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `sistema`.`empleados` WHERE id=%s", (id))
    conn.commit()
    return redirect('/')

#Edita información de un empleado en la base de dato previamente cambiado en edit.
@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    id=request.form['txtID']

    sql = 'UPDATE `sistema`.`empleados` SET `nombre`=%s, `correo`=%s WHERE id=%s;'
    datos = (_nombre, _correo, id)

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')

    if _foto.filename!='':
        nuevo_nombre_foto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevo_nombre_foto)

        cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE id=%s", id)
        fila= cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE `sistema`.`empleados` SET foto=%s WHERE id=%s", (nuevo_nombre_foto, id))
        conn.commit()

    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

#Formulario para editar información de los empleados
@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `sistema`.`empleados` WHERE id=%s", (id))
    empleados = cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)

if __name__ == '__main__':
    app.run(debug=True)