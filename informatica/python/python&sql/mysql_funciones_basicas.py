import pymysql

class Database:
    def __init__(self): #este es el constructor de la clase
        # se conecta
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='alumno'
        )

        self.cursor = self.connection.cursor()
        print("Conexión Exitosa")

    def insert (self,matr,fname,lname,div,nac):
        #inserta un registro
        cmd = "INSERT INTO alumno VALUES ({}, '{}', '{}', {}, '{}')".format(matr, fname, lname, div, nac)
        self.cursor.execute(cmd)
        self.connection.commit()
        

    def create_table (self):                    
        # Crea una tabla alumnos
        cmd = "CREATE TABLE alumno (mat INT(5),fname VARCHAR(20),lname VARCHAR(30),divi INT(3),nac DATE,PRIMARY KEY(mat));"
        self.cursor.execute(cmd)
                
    
    def print(self):
        #imprime todos los registros de la tabla alumno
        cmd ="SELECT * FROM alumno"
        self.cursor.execute(cmd) # El cursor ejecuta el comando de arriba
        r = self.cursor.fetchall()               # Toma todo el contenido de la tabla y lo guarda en r
        for i in r:     # i toma todos los valores de r  
            print (i)

    
database = Database()
#database.create_table()
database.insert(15566,'Fabrizio','Carlassara',722,'1997-02-14')
database.print()
