import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup
import datetime
import wikipediaapi

bot = Bot(token="6452953463:AAFsYV2w8r8-mt28ad8u4Sq9LJK0CeCiEOg")
dp = Dispatcher(bot)

# Замените на ваш API-ключ OpenWeatherMap
OPENWEATHERMAP_API_KEY = "5fc9bfd10569be5ab91597a7a3cd1c24"

# Инициализируем объект для работы с Wikipedia
wiki_wiki = wikipediaapi.Wikipedia(
    language='ru',  # Указываем язык
    user_agent="MyCoolBot/1.0"  # Задаем User-Agent
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Че как, я твой новый эхо бот!")

@dp.message_handler()
async def echo(message: types.Message):
    user_text = message.text.lower()

    response = ""

    if "сколько время?" in user_text:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"Текущее время: {current_time}"
    elif "день недели?" in user_text:
        current_date = datetime.datetime.now().strftime("%A, %d %B, %Y года")
        response = f"Сегодня {current_date}"
    elif "сколько стоит биткоин?" in user_text:
        bitcoin_price = get_bitcoin_price()
        response = f"Текущая цена биткоина: ${bitcoin_price}"
    elif "погода в алматы" in user_text:
        weather_forecast = get_weather_forecast()
        response = weather_forecast
    elif user_text.startswith("определи это"):
        search_query = user_text[13:].strip()  # Извлекаем запрос для поиска в Википедии
        wikipedia_response = get_wikipedia_summary(search_query)
        response = wikipedia_response
    else:
        try:
            result = eval(user_text)
            response = f"Результат: {result}"
        except Exception:
            response = user_text

    await message.answer(response)

def get_bitcoin_price():
    url = "https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json()
    bitcoin_price = data.get("price")
    return bitcoin_price

def get_weather_forecast():
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Almaty&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        response = f"Погода в Алматы: Температура: {temperature}°C, {weather_description.capitalize()}"
    else:
        response = "Не удалось получить прогноз погоды."

    return response

def get_wikipedia_summary(search_query):
    page = wiki_wiki.page(search_query)
    if page.exists():
        summary = page.summary
        return summary
    else:
        return "Информация не найдена в Википедии."

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
