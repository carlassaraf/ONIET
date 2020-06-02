# Este codigo es un ejemplo sencillito de como vincular un bot de Telegram con
# una base de datos de SQL.
# Lo unico que este bot puede hacer es un SELECT * FROM table

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pymysql as sq
from config.auth import token # Incluye el token del bot

# Establezco la conexion con la database
connection = sq.connect(
    host='localhost',
    user='root',
    password='',
    db='alumnosdb'
)

# Inicializo el cursor para los comandos de SQL
cursor = connection.cursor()

# Callback para el comando /start en el bot
def start(bot, update):

    bot.send_message(
        chat_id = update.message.chat_id,
        text = "Hola"
    )

# Callback para el comando /fetchall
def fetchall(bot, update):

    cmd = """SELECT * FROM alumno"""
    cursor.execute(cmd)
    
    table = formatTable(cursor.fetchall())
    print (table)

    bot.send_message(
        chat_id = update.message.chat_id,
        text = table
    )    

# Para darle formato a lo que recuperemos de la database
def formatTable(table):

    txt = ""
    for i in table:
        txt += "Matricula: " + str(i[0]) + "\n"
        txt += "Alumno: " + i[1] + " " + i[2] + "\n"
        txt += "Curso: " + str(i[3]) + "\n"
        txt += "Nacimiento: " + str(i[4]) + "\n\n"

    return txt

# Callback para atender cualquier tipo de mensajes que reciba el bot
def msg(bot, update):

    bot.send_message(
        chat_id = update.message.chat_id,
        text = "No entiendo ese comando."
    )    

if __name__ == '__main__':

    # El objeto updater va a tener el paquete de datos que le llega al bot con cada mensaje
    updater = Updater(token=token)

    # El objeto dispatcher se va a encargar de escuchar el chat
    dispatcher = updater.dispatcher

    # El CommandHandler se encarga de vincular el comando con una funcion
    dispatcher.add_handler(CommandHandler('start',start))
    dispatcher.add_handler(CommandHandler('fetchall',fetchall))

    # El MessageHandler hace lo mismo pero con cualquier tipo de mensajes,
    # en este caso no filtramos ningun formato de mensaje en particular
    dispatcher.add_handler(MessageHandler(Filters.all,msg))

    updater.start_polling()
    updater.idle()