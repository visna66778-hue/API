
import requests
import json
import os
import time


FILE_NAME = "currency_rate.json"


def get_currency_rates(base: str) -> dict:
    url = f"https://open.er-api.com/v6/latest/{base}"

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()

        if data.get("result") == "success":
            return data

        raise ValueError("Не удалось получить курсы валют.")

    raise ValueError(
        f"Ошибка сервера: {response.status_code}"
    )


def save_to_file(data: dict, path="currency_rate.json"):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(f"Данные сохранены в {path}")


def read_from_file(path="currency_rate.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def is_cache_valid(path="currency_rate.json"):
    if not os.path.exists(path):
        return False

    file_age = time.time() - os.path.getmtime(path)

    return file_age < 24 * 60 * 60


def main():
    base = input(
        "Введите базовую валюту (например, USD): "
    ).strip().upper()

    if not base:
        print("Необходимо ввести базовую валюту.")
        return

    try:
        if is_cache_valid():
            data = read_from_file()

            if data.get("base_code") == base:
                print("Используем сохранённые курсы.")
            else:
                print(
                    "В файле другая базовая валюта. "
                    "Обновляем данные."
                )

                data = get_currency_rates(base)
                save_to_file(data)

        else:
            print(
                "Файл отсутствует или устарел. "
                "Обновляем курсы."
            )

            data = get_currency_rates(base)
            save_to_file(data)

        rates = data["rates"]

        print(f"\nКурсы относительно {base}:")

        for currency in ["RUB", "EUR", "GBP"]:
            if currency in rates:
                print(f"{currency}: {rates[currency]}")
            else:
                print(f"Курс {currency} недоступен.")

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        OSError
    ) as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
