class Information:
    def getAbout(self, bot, update):
        describe = "Данный бот оповещает пользователя свежей информацией о погоде и новостям\n/weather - узнать погоду (вводите свой город в формате 'Penza')\n/rnews - региональные новости\n/gnews - новости мира"
        bot.sendMessage(chat_id=update.message.chat_id, text=describe)