import Weather, News, Config, Info
import telegram, logging, pyowm
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pyowm import OWM

updater = Updater(token = Config.BOT_TOKEN)
owm = OWM(Config.WEATHER_TOKEN, language = 'ru')

root = logging.getLogger()
root.setLevel(logging.INFO)

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  level = logging.INFO)

logger = logging.getLogger(__name__)

# @bot.message_handler(content_types=["text"])
# def feedback(message):
#     bot.send_message(message.chat.id, message.text)

def main():
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", Info.getAbout))
    dp.add_handler(CommandHandler("start", Info.getAbout))
    dp.add_handler(CommandHandler("rnews", News.getRegionNews))
    dp.add_handler(CommandHandler("gnews", News.getNews_List))
    dp.add_handler(CommandHandler("weather", Weather.start))
    dp.add_handler(MessageHandler([Filters.text], Weather.city))
    dp.add_handler(CommandHandler('delete', Weather.delete, pass_args=True))
    dp.add_handler(MessageHandler([Filters.command], Weather.unknown))
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
