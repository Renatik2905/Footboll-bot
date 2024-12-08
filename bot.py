import config
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from random import randint
import sqlite3 

bot = telebot.TeleBot(config.API_TOKEN)

def senf_info(bot, message, row):
        
        info = f"""
⚽Этап:   {row[0]}
⚽Раунд:   {row[1]}
⚽Группа:  {row[2]}
⚽Дата:    {row[3]}
⚽Команда_1:  {row[4]}
⚽Первый тайм:      {row[5]}
⚽Второй тайм:      {row[6]}
⚽Команда_2:  {row[7]}
"""
        bot.send_message(message.chat.id, info)



def main_markup():
  markup = ReplyKeyboardMarkup()
  markup.add(KeyboardButton('/random'))
  return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """Привет(●'◡'●)! Добро пожаловать в программу по евофутболу⚽⚽⚽!
Здесь вы можете узнать даты проведения матчей за 2010-11 год и их разельтаты 🔥
Нажмите /random, чтобы получить результат случайного матча
Или напишите название команды или другую информацию, и я постараюсь найти матч который тебе нужен! ⚽ """, reply_markup=main_markup())

@bot.message_handler(commands=['random'])
def random_movie(message):
    con = sqlite3.connect("champs.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM league ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchall()[0]
        cur.close()
    senf_info(bot, message, row)

    
@bot.message_handler(func=lambda message: True)
def echo_message(message):

    con = sqlite3.connect("champs.db")
    with con:
        cur = con.cursor()
        cur.execute(f"select * from league where LOWER(Team_1) = '{message.text.lower()}'")
        row = cur.fetchall()
        if row:
            row = row[0]
            bot.send_message(message.chat.id,"Конечно, у меня немного информации об этом😉 ")
            senf_info(bot, message, row)
        else:
            bot.send_message(message.chat.id,"Увы😥 я не знаю такого матча ")

        cur.close()



bot.infinity_polling()
