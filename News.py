import urllib.request
import requests
from bs4 import BeautifulSoup
import Config, BotInf
import telegram, pyowm
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pyowm import OWM

news_list=0

def getNews_List(bot, update):
    r = requests.get("http://yandex.ru")
    soup = BeautifulSoup(r.text, "html.parser")
    news = soup.find_all(class_="link list__item-content link_black_yes")
    for new_cur in news[0:5]:
        news_list = (new_cur.get("aria-label"))
        bot.sendMessage(chat_id=update.message.chat_id, text="• " + news_list)


def getRegionNews(bot, update):
    r = requests.get("http://yandex.ru")
    soup = BeautifulSoup(r.text, "html.parser")
    news = soup.find_all(class_="link list__item-content link_black_yes")
    for new_cur in news[5:10]:
        region_list = new_cur.get("aria-label")
        bot.sendMessage(chat_id=update.message.chat_id, text="• " + region_list)
