import Config, BotInf, Info
import telegram, pyowm
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pyowm import OWM

hide_markup = telegram.ReplyKeyboardHide()

towns = []
town_keyboard = [['Помощь'], towns]
town_markup = telegram.ReplyKeyboardMarkup(town_keyboard, resize_keyboard=True)

remove_towns = []
remove_keyboard = [remove_towns]
remove_markup = telegram.ReplyKeyboardMarkup(remove_keyboard, resize_keyboard=True)

helpmessages = Info.describe

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Введите город для сохранения", reply_markup=town_markup)


def city(bot, update):
    message = update.message
    chat_id = message.chat_id
    text = message.text

    if text == "Remove city":
        bot.sendMessage(chat_id=chat_id, text="Выберите город который хотите удалить", reply_markup=remove_markup)
    elif text == "Помощь":
        bot.sendMessage(chat_id=chat_id, text=helpmessages, reply_markup=town_markup)
    else:
        if len(towns) == 0:
            towns.append(text)
            remove_towns.append("/delete " + text)
            town_keyboard.append(["Remove city"])
            town_keyboard.remove(["Помощь"])
            bot.sendMessage(chat_id=chat_id, text="Сохранили", reply_markup=town_markup)
        elif len(towns) == 1:
            if text == towns[0] and "/delete " + text == remove_towns[0]:
                get_weather(bot, update, text)
            else:
                towns.append(text)
                remove_towns.append("/delete " + text)
                bot.sendMessage(chat_id=chat_id, text="Сохранили", reply_markup=town_markup)
        elif len(towns) == 2:
            if (text == towns[0] or text == towns[1]) and (
                        "/delete " + text == remove_towns[0] or "/delete " + text == remove_towns[1]):
                get_weather(bot, update, text)
            else:
                towns.append(text)
                remove_towns.append("/delete " + text)
                bot.sendMessage(chat_id=chat_id, text="Сохранили", reply_markup=town_markup)
        else:
            get_weather(bot, update, text)


def get_weather(bot, update, text):
    obs = BotInf.owm.weather_at_place(text)
    w = obs.get_weather()
    temp = str(round(w.get_temperature(unit='celsius').get('temp')))
    status = str(w.get_detailed_status())
    bot.sendMessage(chat_id=update.message.chat_id, text="Температура: " + temp + ", состояние погоды: " + status)


def delete(bot, update, args):
    message = update.message
    chat_id = message.chat_id

    try:
        towns.remove(args[0])
        remove_towns.remove("/delete " + args[0])
        if len(towns) == 0:
            town_keyboard.remove(["Remove city"])
            town_keyboard.append(["Помощь"])
        bot.sendMessage(chat_id=chat_id, text="Город удален", reply_markup=town_markup)
    except ValueError:
        bot.sendMessage(chat_id=chat_id, text="Этого города не существует", reply_markup=town_markup)


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Неизвестная команда")
