import requests
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

API_KEY = os.getenv("API_KEY")



def get_current_weather(city: str = None, latitude: float = None, longitude: float = None) -> dict:
    if city:
        print(f"Получаем погоду для города {city}")
        coordinates = get_coordinates(city)

        if coordinates is None:
            return None

        latitude, longitude = coordinates
        return get_weather_by_coordinates(latitude, longitude)

    if latitude is not None and longitude is not None:
        print(f"Получаем погоду для координат: {latitude}, {longitude}")
        return get_weather_by_coordinates(latitude, longitude)

    return None


def get_coordinates(city: str) -> tuple:
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "appid": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data:
            return data[0]["lat"], data[0]["lon"]

        print("Город не найден")
        return None

    else:
        print(f"Ошибка: {response.status_code}")
        return None


def get_weather_by_coordinates(latitude: float, longitude: float) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка: {response.status_code}")
        return None


    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

    else:
        print(f"Ошибка: {response.status_code}")
        return None


if __name__ == "__main__":
    city = input("Введите город: ")
    weather = get_current_weather(city)

    if weather:
        print(f"Погода в {weather['name']}: {weather['main']['temp']}°C, {weather['weather'][0]['description']}")