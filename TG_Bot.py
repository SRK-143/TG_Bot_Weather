import telebot
import requests
import logging
import psycopg2

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot('7859888796:AAHaFL7H3LCmVie4Kz6hepHQh6zIfKGbyNs')

start_txt = 'Привет! Этот бот создан в качестве теста для компании BobrAi. Используй команду <город>, чтобы получить текущий прогноз погоды.'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def weather(message):
    city = message.text
    url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    weather_data = requests.get(url).json()
    print(weather_data)
    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])

    w_now = 'Сейчас в городе ' + city + ' ' + str(temperature) + ' °C'
    w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
    w_discr = str(weather_data['weather'][0]['description'])
    w_hum = "Влажность " +str(weather_data['main']['humidity']) + " %"
    w_wind = "Скорость ветра "+str(weather_data["wind"]["speed"]) + " м/с"

    bot.send_message(message.from_user.id, w_now)
    bot.send_message(message.from_user.id, w_feels)
    bot.send_message(message.from_user.id, w_discr)
    bot.send_message(message.from_user.id, w_hum)
    bot.send_message(message.from_user.id, w_wind)

    logger.info(city)
    logger.info(message.from_user.id)
    logger.info(w_now)
    logger.info(w_feels)
    logger.info(w_discr)
    logger.info(w_hum)
    logger.info(w_wind)

    log_info = w_now + '\n' + w_feels + '\n' + w_discr + '\n' + w_hum + '\n' + w_wind

    log_to_db(message.from_user.id, city, log_info)

bd = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Cgfkmybr36",
    "host": "localhost",
    "port": "5432"
}

def log_to_db(user_id, command, response):
    conn = psycopg2.connect(**bd)
    cur = conn.cursor()

    insert_query = '''
    INSERT INTO Weather_data (user_id, command, response)
    VALUES (%s, %s, %s);
    '''

    cur.execute(insert_query, (user_id, command, response))
    conn.commit()

    cur.close()
    conn.close()
    print("Данные успешно добавлены в таблицу Weather_data.")

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')