import requests
from bs4 import BeautifulSoup

class News: #класс новостей

    def getGlobalNews(self, bot, update): # получить новости из мира
        r = requests.get("http://yandex.ru")
        soup = BeautifulSoup(r.text, "html.parser")
        news = soup.find_all(class_="link list__item-content link_black_yes")
        for new_cur in news[0:5]:
            news_list = (new_cur.get("aria-label"))
            bot.sendMessage(chat_id=update.message.chat_id, text="• " + news_list)


    def getRegionNews(self,bot, update): # получить региональные новости
        r = requests.get("http://yandex.ru")
        soup = BeautifulSoup(r.text, "html.parser")
        news = soup.find_all(class_="link list__item-content link_black_yes")
        for new_cur in news[5:10]:
            region_list = new_cur.get("aria-label")
            bot.sendMessage(chat_id=update.message.chat_id, text="• " + region_list)
