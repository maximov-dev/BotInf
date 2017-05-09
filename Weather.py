import Config, BotInf, Info
import telegram.ext, pyowm
from telegram.ext import updater
from telegram import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pyowm import OWM

class WeatherApp():
    def __init__(self):
        hide_markup = telegram.ReplyKeyboardHide()
        self.towns=[]
        self.town_keyboard = [['Помощь'], self.towns]
        self.town_markup = telegram.ReplyKeyboardMarkup(self.town_keyboard, resize_keyboard=True)
        self.remove_towns = []
        self.remove_keyboard = [self.remove_towns]
        self.remove_markup = telegram.ReplyKeyboardMarkup(self.remove_keyboard, resize_keyboard=True)
        self.message = update.message
        self.chat_id = self.message.chat_id
        self.text = self.message.text
        self.helpmessages = "Данный бот оповещает пользователя свежей информацией о погоде и новостям в регионе\n/weather - узнать погоду (вводите свой город в формате 'Penza')\n/rnews - региональные новости\n/gnews - новости мира"


    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Введите город для сохранения", reply_markup=self.town_markup)

    def city(self, bot, update):
        if self.text == "Remove city":
            bot.sendMessage(chat_id=self.chat_id, text="Выберите город который хотите удалить", reply_markup=self.remove_markup)
        elif self.text == "Помощь":
            bot.sendMessage(chat_id=self.chat_id, text= self.helpmessages, reply_markup=self.town_markup)
        else:
            if len(self.towns) == 0:
                self.towns.append(self.text)
                self.remove_towns.append("/delete " + self.text)
                self.town_keyboard.append(["Remove city"])
                self.town_keyboard.remove(["Помощь"])
                bot.sendMessage(chat_id=self.chat_id, text="Сохранили", reply_markup=self.town_markup)
            elif len(self.towns) == 1:
                if self.text == self.towns[0] and "/delete " + self.text == self.remove_towns[0]:
                    WeatherApp.get_weather(bot, update, self.text)
                else:
                    self.towns.append(self.text)
                    self.remove_towns.append("/delete " + self.text)
                    bot.sendMessage(chat_id=self.chat_id, text="Сохранили", reply_markup=self.town_markup)
            elif len(self.towns) == 2:
                if (self.text == self.towns[0] or self.text == self.towns[1]) and (
                            "/delete " + self.text == self.remove_towns[0] or "/delete " + self.text == self.remove_towns[1]):
                    WeatherApp.get_weather(bot, update, self.text)
                else:
                    self.towns.append(self.text)
                    self.remove_towns.append("/delete " + self.text)
                    bot.sendMessage(chat_id=self.chat_id, text="Сохранили", reply_markup=self.town_markup)
            else:
                WeatherApp.get_weather(bot, update, self.text)


    def get_weather(self, bot, update, text):
        obs = BotInf.owm.weather_at_place(text)
        w = obs.get_weather()
        temp = str(round(w.get_temperature(unit='celsius').get('temp')))
        status = str(w.get_detailed_status())
        bot.sendMessage(chat_id=update.message.chat_id, text="Температура: " + temp + ", состояние погоды: " + status)


    def delete(self, bot, update, args):
        try:
            self.towns.remove(args[0])
            self.remove_towns.remove("/delete " + args[0])
            if len(self.towns) == 0:
                self.town_keyboard.remove(["Remove city"])
                self.town_keyboard.append(["Помощь"])
            bot.sendMessage(chat_id=self.chat_id, text="Город удален", reply_markup=self.town_markup)
        except ValueError:
            bot.sendMessage(chat_id=self.chat_id, text="Этого города не существует", reply_markup=self.town_markup)


    def unknown(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Неизвестная команда")