from flask import Flask, render_template, request, redirect
import pymysql as sq

app = Flask(__name__) # Le dice a Flask que esta es la aplicacion principal
connection = sq.connect(
    host='localhost',
    user='root',
    password='',
    db='alumnosdb'
)
cursor = connection.cursor()

table_fields = {
    "mat"   : "Matricula",
    "fname" : "Nombre",
    "lname" : "Apellido",
    "divi"  : "Curso",
    "nac"   : "Nacimiento"
}

last_consult = []   # Variable global para registrar la ultima consulta

""" Funciones de SQL (CREATE, DROP, INSERT, SELECT * FROM, DELETE) """

# Ejecuta un CREATE TABLE ...
def create():
    cmd = "CREATE TABLE alumno (mat INT(5),fname VARCHAR(20),lname VARCHAR(30),divi INT(3),nac DATE,PRIMARY KEY(mat));"
    cursor.execute(cmd)

# Ejecuta un DROP TABLE ...
def drop():
    cursor.execute("DROP TABLE alumno")

# Ejecuta un INSERT INTO ... VALUES
def insert(datos):
    cmd = """INSERT INTO alumno VALUES ({}, '{}', '{}', {}, '{}')""".format(
    datos[4], datos[0], datos[1], datos[3], datos[2])
    try:
        cursor.execute(cmd)
        connection.commit() # No se olviden de esto o los cambios no se guardan :)
    except sq.Error:
        return render_template("loadForm.html")
        # Donde van las llaves, van los datos que entran como parametros

# Ejecuta un SELECT * FROM ... WHERE 
def fetch(where,what):
    cmd = """SELECT * FROM alumno WHERE {} = '{}'""".format(where,what)
    cursor.execute(cmd)
    return cursor.fetchall()

# Ejecuta un SELECT * FROM ...
def fetch_all():
    cursor.execute("""SELECT * FROM alumno""")
    return cursor.fetchall()

# Actualiza la consulta y devuelve las coincidencias
def consultBy(field):
    global last_consult
    if request.method == "POST":    # Chequea que el metodo fue un posteo del form en el server
        req = request.form

        for i in req.items():
            f=fetch(field,i[1])
            last_consult = i
            return f
    return render_template('loadForm.html')

# Ejecuta un DELETE FROM ... WHERE
def deleteBy():
    global last_consult
    if request.method == "POST":    # Chequea que el metodo fue un posteo del form en el server
        req = request.form
        
        for i in req.items():
            cmd = """DELETE FROM alumno WHERE mat = {}""".format(i[1])
            print (cmd)
            cursor.execute(cmd)
            connection.commit()
            return fetch_all()#fetch(last_consult[0],last_consult[1])
    return render_template('loadForm.html')    

# Ejecuta un UPDATE ... SET ... WHERE
def set():
    global last_consult
    req = request.form
    try: 
        aux = []
        for i in req.items():
            
            if i[1] != "" and i[0] != 'where':  # El formulario me va a enviar los cinco campos, solamente ejecuto el comando para los campos que esten llenos
                aux.append("{} = '{}'".format(i[0],i[1]))
        cmd = """UPDATE alumno SET """ + ', '.join(aux) + " WHERE mat = {}".format(i[1]) + ';'
        print (cmd)
        cursor.execute(cmd)
        connection.commit()
        return fetch_all()#fetch(last_consult[0],last_consult[1])
    except IndexError:
        print ("No se hizo una consulta previa")
        return render_template('loadForm.html', feedbackUpdate = "No se hizo consulta previa.")
    return render_template('loadForm.html')

""" Rutas de navegacion de la pagina """ 

# El @ es un decorador pero no se que hace
@app.route('/') # Creo una ruta para la pagina principal
def home():
    return render_template('home.html') # Llama un codigo de html

@app.route('/load', methods=["GET", "POST"])
def load():
    if request.method == "POST":    # Chequea que el metodo fue un posteo del form en el server
        req = request.form
        missing = list()

        for k, v in req.items():
            if v ==  "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("loadForm.html", feedback=feedback)
        else:
            dat = []
            for i in req.items():
                dat.append(i[1])
            insert(dat)
    table = fetch_all()
    return render_template('loadForm.html', table=table)

@app.route('/view')
# Muestra la tabla entera
def database():
    table = fetch_all()
    return render_template('view.html', table=table)

""" Consult related routes """

@app.route('/consult')
# Llama al html de consultas
def consult():
    return render_template('loadForm.html')   

@app.route('/consult-type', methods=["GET", "POST"])
# Se fija el campo que se eligio consultar y actualiza la vista html
def consult_sel():
    req = request.form    
    table = fetch_all()
    for i in req.items():
        return render_template('loadForm.html', consult=[table_fields[i[0]], i[0]], table=table)  # Llamo el html con el identificador de la consulta para llenar un label

@app.route('/consult-init', methods=["GET", "POST"])    
# Inicia una consulta
def consult_init():
    req = request.form
    for i in req.items():
        table = consultBy(i[0])
        return render_template('loadForm.html', table=table) 

@app.route('/update', methods=["POST"])
# Hace un update de un registro y devuelve la tabla nueva
def update():
    table = set()
    return render_template("loadForm.html", table=table)

""" Create, drop and delete routes """

@app.route('/create')
# Crea una tabla nueva
def create_table():
    create()
    return render_template('loadForm.html')

@app.route('/drop')
# Elimina la tabla actual
def drop_table():
    drop()
    return render_template('loadForm.html')

@app.route('/delete', methods=["POST"])
# Elimina un registro y actualiza la tabla
def delete():
    table = deleteBy()
    return render_template('loadForm.html',table=table)

if __name__ == '__main__':  # Verifico que sea el archivo principal y no un modulo
    app.run(debug=True) # Le aviso que estoy armando la pagina y se va a reiniciar el servidor cada vez que haya cambios
