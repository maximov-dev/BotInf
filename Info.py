import Weather, News, Config
import telegram, logging, pyowm
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pyowm import OWM
describe="Данный бот оповещает пользователя свежей информацией о погоде и новостям в регионе\n/weather - узнать погоду (вводите свой город в формате 'Penza')\n/rnews - региональные новости\n/gnews - новости мира"

def getAbout(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=describe)