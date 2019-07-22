import BotInf, Config, Info
import telegram, pyowm
from pyowm import OWM

owm = OWM(Config.WEATHER_TOKEN, language='ru')
# Скрытие клавиатуры по ненадобности
hide_markup = telegram.ReplyKeyboardRemove()

# Список городо в списке(основная клавиатура)
towns = []
town_keyboard = [['Помощь'], towns]
town_markup = telegram.ReplyKeyboardMarkup(town_keyboard, resize_keyboard = True)

# Список городов для их удаления из основного списка
remove_towns = []
remove_keyboard = [remove_towns]
remove_markup = telegram.ReplyKeyboardMarkup(remove_keyboard, resize_keyboard = True)

class WeatherApp: # погода
    # запуск работы с погодой
    def start(self, bot, update):
        bot.sendMessage(chat_id = update.message.chat_id, text = "Введите город для сохранения", reply_markup = town_markup)

    # Функция отвечающая заопределение команд которые вводит пользователь боту
    def city(self, bot, update):
        message = update.message
        chat_id = message.chat_id
        text = message.text

        if text == "Remove city":
            bot.sendMessage(chat_id = chat_id, text = "Выберите город который хотите удалить", reply_markup = remove_markup)
        elif text == "Помощь":
            bot.sendMessage(chat_id = chat_id, text = Info.Information.getAbout(self, bot, update), reply_markup = town_markup)
        else:
            if len(towns) == 0:
                towns.append(text)
                remove_towns.append("/delete " + text)
                town_keyboard.append(["Remove city"])
                town_keyboard.remove(["Помощь"])
                bot.sendMessage(chat_id = chat_id, text = "Сохранили", reply_markup = town_markup)
            elif len(towns) == 1:
                if text == towns[0] and "/delete " + text == remove_towns[0]:
                    WeatherApp.get_weather(self, bot, update, text)
                else:
                    towns.append(text)
                    remove_towns.append("/delete " + text)
                    bot.sendMessage(chat_id = chat_id, text = "Сохранили", reply_markup = town_markup)
            elif len(towns) == 2:
                if (text == towns[0] or text == towns[1]) and ("/delete " + text == remove_towns[0] or "/delete " + text == remove_towns[1]):
                    WeatherApp.get_weather(self, bot, update, text)
                else:
                    towns.append(text)
                    remove_towns.append("/delete " + text)
                    bot.sendMessage(chat_id = chat_id, text = "Сохранили", reply_markup = town_markup)
            else:
                WeatherApp.get_weather(self, bot, update, text)

    # метод получения погоды
    def get_weather(self, bot, update, text):
        obs = owm.weather_at_place(text)
        w = obs.get_weather()
        temp = str(round(w.get_temperature(unit='celsius').get('temp')))
        status = str(w.get_detailed_status())
        bot.sendMessage(chat_id=update.message.chat_id, text = "Температура: " + temp +", состояние погоды: " + status)

    # метод удаления города из основного списка
    def delete(self, bot, update, args):
        message = update.message
        chat_id = message.chat_id

        # проверка на существование города
        try:
            towns.remove(args[0])
            remove_towns.remove("/delete " + args[0])
            if len(towns) == 0:
                town_keyboard.remove(["Remove city"])
                town_keyboard.append(["Помощь"])
            bot.sendMessage(chat_id = chat_id, text = "Город удален", reply_markup = town_markup)
        except ValueError:
            bot.sendMessage(chat_id = chat_id, text = "Этого города не существует", reply_markup = town_markup)

    # метод, отвечающий за вывод ошибки при вводе несуществующей комманды
    def unknown(self, bot, update):
        bot.sendMessage(chat_id = update.message.chat_id, text = "Неизвестная команда")