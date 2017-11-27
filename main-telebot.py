# -*- coding: utf-8 -*-

import telebot
import config
from dbutils import DB
from telebot import types

from telegramcalendar import create_calendar
import datetime
CAPTION_BTN_NEW = "Hовая заявка"
bot = telebot.TeleBot(config.token)
current_shown_dates={}
db = DB()

# def add_keyboard():
#     # Эти параметры для клавиатуры необязательны, просто для удобства
#     keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
#     button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
#     keyboard.add(button_phone, button_geo)

# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_new_notice = types.KeyboardButton(text=CAPTION_BTN_NEW)
    cnt = db.get_notice_cnt(message.chat.id)
    btn_my_notice = types.KeyboardButton(text="Mои заявки({cnt})".format(cnt=cnt))
    keyboard.add(btn_new_notice, btn_my_notice)
    msg_s = """
Доброго времени, {user_name}!

Необходимо доставить груз?
Тогда просто оставьте заявку! :)
            """
    msg_s = msg_s.format(user_name=message.from_user.first_name)
    bot.send_message(message.chat.id, msg_s, reply_markup=keyboard)

    # state = db.get_user_state(message.chat.id)
    # if state == config.States.ENTER_NAME_S:
    #     bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить своё имя, но так и не сделал этого :( Жду...")
    # elif state == config.States.ENTER_AGE_S:
    #     bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить свой возраст, но так и не сделал этого :( Жду...")
    # elif state == config.States.SEND_PIC_S:
    #     bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить картинку, но так и не сделал этого :( Жду...")
    # else:  # Под "остальным" понимаем состояние "0" - начало диалога
        
    #     db.set_user_state(message.chat.id, config.States.ENTER_NAME_S, message.from_user.first_name)


@bot.message_handler(commands=['calendar'])
def get_calendar(message):
    now = datetime.datetime.now() #Current date
    chat_id = message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = date #Saving the current date in a dict
    markup= create_calendar(now.year,now.month)
    bot.send_message(message.chat.id, "Выберите дату готовности груза", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        day=call.data[13:]
        date = datetime.datetime(int(saved_date[0]),int(saved_date[1]),int(day),0,0,0)
        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, str(date))
        bot.answer_callback_query(call.id, text="Хорошо")

    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Выберите дату готовности груза", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month-=1
        if month<1:
            month=12
            year-=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Выберите дату готовности груза", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def ignore(call):
    bot.answer_callback_query(call.id, text="")



# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    print('cmd_reset')
    # Эти параметры для клавиатуры необязательны, просто для удобства
    
    # db.set_user_state(message.chat.id, config.States.ENTER_NAME_S, message.from_user.first_name)

@bot.message_handler(func=lambda message: db.get_user_state(message.chat.id) == config.States.NEW_NOTICE_ADDRESS_S)
def user_entering_address(message):
    # В случае с именем не будем ничего проверять, пусть хоть "25671", хоть Евкакий
    bot.send_message(message.chat.id, "Отличное адрес! Теперь укажи, пожалуйста,  вес(в килограммах):")
    db.set_user_state(message.chat.id, config.States.NEW_NOTICE_MASS_S, message.from_user.first_name)


@bot.message_handler(content_types=["text"])
def user_start(message):
    print("user_startuser_start")
    print(current_shown_dates)
    print(message.message_id)
    if message.text.encode('utf-8') == CAPTION_BTN_NEW:
        print('CAPTION_BTN_NEW')
        bot.send_message(message.chat.id, "Введите адрес доставки", reply_markup=types.ReplyKeyboardRemove())
        db.set_user_state(message.chat.id, config.States.NEW_NOTICE_ADDRESS_S, message.from_user.first_name)
    # В случае с именем не будем ничего проверять, пусть хоть "25671", хоть Евкакий




# @bot.message_handler(func=lambda message: db.get_user_state(message.chat.id) == config.States.ENTER_AGE_S)
# def user_entering_age(message):
#     # А вот тут сделаем проверку
#     if not message.text.isdigit():
#         # Состояние не меняем, поэтому только выводим сообщение об ошибке и ждём дальше
#         bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
#         return
#     # На данном этапе мы уверены, что message.text можно преобразовать в число, поэтому ничем не рискуем
#     if int(message.text) < 5 or int(message.text) > 100:
#         bot.send_message(message.chat.id, "Какой-то странный возраст. Не верю! Отвечай честно.")
#         return
#     else:
#         # Возраст введён корректно, можно идти дальше
#         bot.send_message(message.chat.id, "Когда-то и мне было столько лет...эх... Впрочем, не будем отвлекаться. "
#                                           "Отправь мне какую-нибудь фотографию.")
#         db.set_user_state(message.chat.id, config.States.SEND_PIC_S, message.from_user.first_name)


# @bot.message_handler(content_types=["photo"],
#                      func=lambda message: db.get_user_state(message.chat.id) == config.States.SEND_PIC_S)
# def user_sending_photo(message):
#     # То, что это фотография, мы уже проверили в хэндлере, никаких дополнительных действий не нужно.
#     bot.send_message(message.chat.id, "Отлично! Больше от тебя ничего не требуется. Если захочешь пообщаться снова - "
#                      "отправь команду /start или /reset.")
#     db.set_user_state(message.chat.id, config.States.START_S, message.from_user.first_name)


if __name__ == "__main__":
    bot.polling(none_stop=True)
