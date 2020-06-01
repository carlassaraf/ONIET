from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pymysql as sq

token = "1193099855:AAG2tnpERT3-HfSRBTw7a3XuJleC5CCk7_Q"

connection = sq.connect(
    host='localhost',
    user='root',
    password='',
    db='alumnosdb'
)

cursor = connection.cursor()

def start(bot, update):

    bot.send_message(
        chat_id = update.message.chat_id,
        text = "Hola"
    )

def fetchall(bot, update):

    cmd = """SELECT * FROM alumno"""
    cursor.execute(cmd)
    
    table = formatTable(cursor.fetchall())
    print (table)

    bot.send_message(
        chat_id = update.message.chat_id,
        text = table
    )    

def formatTable(table):

    txt = ""
    for i in table:
        txt += "Matricula: " + str(i[0]) + "\n"
        txt += "Alumno: " + i[1] + " " + i[2] + "\n"
        txt += "Curso: " + str(i[3]) + "\n"
        txt += "Nacimiento: " + str(i[4]) + "\n\n"

    return txt
"""
    txt = []
    for i in table:
        txt.append("Matricula: " + i[0] + "\nAlumno: " + 
              i[1] + " " + i[2] + "\nCurso: " + i[3] +
              "Nacimiento: " + i[4])

    return txt
"""

def msg(bot, update):

    bot.send_message(
        chat_id = update.message.chat_id,
        text = "No entiendo ese comando."
    )    

if __name__ == '__main__':

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start',start))
    dispatcher.add_handler(CommandHandler('fetchall',fetchall))

    dispatcher.add_handler(MessageHandler(Filters.all,msg))

    updater.start_polling()
    updater.idle()