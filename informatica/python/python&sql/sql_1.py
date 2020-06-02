""" SQL

    El programa crea una base de datos local. Con esa
    base de datos puede:
        - Crear una tabla 'alumno'.
        - Eliminar la tabla.
        - Insertar un alumno en la tabla.
        - Mostrar todos los contenidos de la tabla.
        
"""
import sqlite3 as sq    # Libreria

connection = sq.connect("escuela.db")   # Establezco conexion con la data base
cursor = connection.cursor()            # Inicializo una instancia de cursor

def create_table ():                    
    # Crea una tabla alumno
    cmd = """CREATE TABLE alumno (
    mat     INT(5),
    fname   VARCHAR(20),
    lname   VARCHAR(30),
    div     INT(3),
    nac     DATE,
    PRIMARY KEY(mat) 
    )"""    
    cursor.execute(cmd) # El cursor ejecuta el comando de arriba

def insert (matr,fname,lname,div,nac):
    # Inserta un nuevo registro en la tabla alumno
    cmd = str.format("""INSERT INTO alumno VALUES ({}, '{}', '{}', {}, '{}')""",
    matr, fname, lname, div, nac)

    # Donde van las llaves, van los datos que entran como parametros
    cursor.execute(cmd)
    connection.commit() # No se olviden de esto o los cambios no se guardan :)

def drop ():
    # Elimina la tabla alumno
    cmd = """ DROP TABLE alumno """
    cursor.execute(cmd)

#drop()
#create_table()

insert (15555,'Fabrizio','Carlassara',722,'1997-02-14')

cmd = """SELECT * FROM alumno"""    # Selecciona la tabla alumno
cursor.execute(cmd)
r = cursor.fetchall()               # Toma todo el contenido de la tabla y lo guarda en r

for i in r:     # i toma todos los valores de r  
    print (i)