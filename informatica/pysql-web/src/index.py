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

last_consult = []

""" Funciones de SQL (CREATE, DROP, INSERT, SELECT * FROM, DELETE) """

def create():
    cmd = "CREATE TABLE alumno (mat INT(5),fname VARCHAR(20),lname VARCHAR(30),divi INT(3),nac DATE,PRIMARY KEY(mat));"
    cursor.execute(cmd)

def drop():
    cursor.execute("DROP TABLE alumno")

def insert(datos):
    # Inserta un nuevo registro en la tabla alumno
    cmd = """INSERT INTO alumno VALUES ({}, '{}', '{}', {}, '{}')""".format(
    datos[4], datos[0], datos[1], datos[3], datos[2])
    try:
        cursor.execute(cmd)
        connection.commit() # No se olviden de esto o los cambios no se guardan :)
    except sq.Error as e:
        return render_template("loadForm.html")
        # Donde van las llaves, van los datos que entran como parametros

def fetch(where,what):
    cmd = """SELECT * FROM alumno WHERE {} = '{}'""".format(where,what)
    cursor.execute(cmd)
    return cursor.fetchall()

def fetch_all():
    cursor.execute("""SELECT * FROM alumno""")
    return cursor.fetchall()

def consultBy(field):
    global last_consult
    if request.method == "POST":    # Chequea que el metodo fue un posteo del form en el server
        req = request.form
        missing = list()

        for k, v in req.items():
            if v ==  "":
                missing.append(k)

            if missing:
                feedback = f"Missing fields for {', '.join(missing)}"
                return render_template("consult.html", feedback=feedback)
            else:
                for i in req.items():
                    f=fetch(field,i[1])
                    last_consult = i
                    return f
        return redirect(request.url)
    return render_template('consult.html')

def deleteBy():
    global last_consult
    if request.method == "POST":    # Chequea que el metodo fue un posteo del form en el server
        req = request.form
        
        for i in req.items():
            cmd = """DELETE FROM alumno WHERE mat = {}""".format(i[1])
            print (cmd)
            cursor.execute(cmd)
            connection.commit()
            return fetch(last_consult[0],last_consult[1])
    return render_template('consult.html')    

def set():
    global last_consult
    if request.method == "POST":    # Chequea que el metodo fue un posteo del form en el server
        req = request.form
        try: 
            for i in req.items():
                if i[1] != "":  # El formulario me va a enviar los cinco campos, solamente ejecuto el comando para el campo que este lleno
                    cmd = """UPDATE alumno SET {} = {} WHERE {} = {};""".format(i[0],i[1],last_consult[0],last_consult[1]) 
                    print (cmd)
                    cursor.execute(cmd)
                    connection.commit()
                    return fetch(last_consult[0],i[1])
        except IndexError:
            print ("No se hizo una consulta previa")
            return render_template('consult.html', feedbackUpdate = "No se hizo consulta previa.")
    return render_template('consult.html')


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
        return redirect(request.url)
    return render_template('loadForm.html')

@app.route('/view')
def database():
    table = fetch_all()
    return render_template('view.html', table=table)

@app.route('/consult')
def consult():
    return render_template('consult.html')

@app.route('/update', methods=["GET", "POST"])
def update():
    table = set()
    return render_template("consult.html", table=table)

""" Rutas de botones """

@app.route('/create', methods=["GET", "POST"])
def create_table():
    create()
    return render_template('loadForm.html')

@app.route('/drop', methods=["GET", "POST"])
def drop_table():
    drop()
    return render_template('loadForm.html')

@app.route('/delete', methods=["GET", "POST"])
def delete():
    table = deleteBy()
    return render_template('consult.html',table=table)

""" Rutas de consulta por campo """

@app.route('/bymat', methods=["GET", "POST"])
def bymat():
    data = consultBy('mat')
    return render_template('consult.html', table=data)

@app.route('/byfname', methods=["GET", "POST"])
def byfname():
    data = consultBy('fname')
    return render_template('consult.html', table=data)

@app.route('/bylname', methods=["GET", "POST"])
def bylname():
    data = consultBy('lname')
    return render_template('consult.html', table=data)

@app.route('/bycurso', methods=["GET", "POST"])
def bycurso():
    data = consultBy('divi')
    return render_template('consult.html', table=data)

@app.route('/bynac', methods=["GET", "POST"])
def bynac():
    data = consultBy('nac')
    return render_template('consult.html', table=data)

if __name__ == '__main__':  # Verifico que sea el archivo principal y no un modulo
    app.run(debug=True) # Le aviso que estoy armando la pagina y se va a reiniciar el servidor cada vez que haya cambios
