import telebot
from telebot import types
import scheduleParser

# bot token's
bot = telebot.TeleBot('***') # each bot have unique token

try:
    @bot.message_handler(commands=['start'])
    def start(message):
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Отправление", callback_data='0')
        keyboard.add(callback_button)
        callback_button1 = types.InlineKeyboardButton(text="Прибытие", callback_data='1')
        keyboard.add(callback_button1)

        bot.send_message(message.chat.id, text="Выберете направление", reply_markup=keyboard)


    @bot.callback_query_handler(func=lambda call: True)
    def find_station(call):
        if call.data == "0":
            scheduleParser.get_main_file(0)
            with open("txt-files/names.txt", 'r', encoding="UTF-8") as file:
                list_of_names = [f"{i + 1}: {item.strip()}" for i, item in enumerate(file)]
                lon = ''
                for i in range(len(list_of_names)):
                    lon += f"{list_of_names[i]}\n"
            bot.send_message(call.message.chat.id, lon)

        elif call.data == "1":
            scheduleParser.get_main_file(1)
            with open("txt-files/names.txt", 'r', encoding="UTF-8") as file:
                list_of_names = [f"{i + 1}: {item.strip()}" for i, item in enumerate(file)]
                lon = ''
                for i in range(len(list_of_names)):
                    lon += f"{list_of_names[i]}\n"
            bot.send_message(call.message.chat.id, str(lon))

        bot.register_next_step_handler(call.message, get_schedule)


    @bot.message_handler(commands=['schedule'])
    def get_schedule(message):
        try:
            bot.send_message(message.chat.id, scheduleParser.get_schedule_station(int(message.text)))
        except Exception as e:
            print("try again! "+str(e))


    bot.polling(none_stop=True)
except Exception as ex:
    print("Sorry, try again! " + str(ex))
