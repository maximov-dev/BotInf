import Weather, News, Config, Info
import telegram, logging, pyowm
from telegram import Update
from telegram.ext import Updater, Filters
from mhandler import MessageHandler
from chandler import CommandHandler

class Bot:
    def __init__(self):
        self.updater = Updater(token = Config.BOT_TOKEN)
        # root = logging.getLogger()
        # root.setLevel(logging.INFO)
        # logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
        # logger = logging.getLogger(__name__)

# @bot.message_handler(content_types=["text"])
# def feedback(message):
#     bot.send_message(message.chat.id, message.text)

    def run(self): # данный метод обеспечивает запуск и работу бота
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler("start", Info.Information.getAbout))
        dp.add_handler(CommandHandler("rnews", News.News.getRegionNews))
        dp.add_handler(CommandHandler("gnews", News.News.getGlobalNews))
        dp.add_handler(CommandHandler("weather", Weather.WeatherApp.start))
        dp.add_handler(MessageHandler([Filters.text], Weather.WeatherApp.city))
        dp.add_handler(CommandHandler('delete', Weather.WeatherApp.delete, pass_args=True))
        dp.add_handler(MessageHandler([Filters.command], Weather.WeatherApp.unknown))
        self.updater.start_polling()
        self.updater.idle()
