
import requests
import json


def print_response(response):
    """Выводит статус и полный JSON-ответ сервера."""

    print("\nСтатус ответа:", response.status_code)
    print("Ответ сервера:")

    try:
        result = response.json()

        print(json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        ))

        return result

    except ValueError:
        print(response.text)
        return None


def get_country_code(country_name):
    """Находит код страны по её названию."""

    url = "https://api.worldbank.org/v2/country"

    params = {
        "format": "json",
        "per_page": 400
    }

    aliases = {
        "vietnam": "viet nam",
        "russia": "russian federation",
        "usa": "united states",
        "uk": "united kingdom",
        "south korea": "korea, rep.",
        "north korea": "korea, dem. people's rep."
    }

    search_name = country_name.strip().casefold()
    search_name = aliases.get(search_name, search_name)

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        result = response.json()

        if not isinstance(result, list) or len(result) < 2:
            return None

        if not result[1]:
            return None

        for country in result[1]:
            if country["name"].casefold() == search_name:
                return country["iso2Code"]

        return None

    except requests.exceptions.RequestException as error:
        print("Ошибка поиска страны:", error)
        return None


def select_country_fields(result):
    """Позволяет пользователю выбирать поля из JSON."""

    if not isinstance(result, list) or len(result) < 2:
        print("Неверная структура JSON.")
        return

    countries = result[1]

    if not isinstance(countries, list) or not countries:
        print("Информация о стране не найдена.")
        return

    country = countries[0]

    fields = {
        "1": ("Название страны", country.get("name")),
        "2": ("Столица", country.get("capitalCity")),
        "3": (
            "Уровень дохода",
            country.get("incomeLevel", {}).get("value")
        ),
        "4": (
            "Регион",
            country.get("region", {}).get("value")
        ),
        "5": ("Долгота", country.get("longitude")),
        "6": ("Широта", country.get("latitude"))
    }

    print("\n===== ВЫБОР ДАННЫХ О СТРАНЕ =====")
    print("1 — Название страны")
    print("2 — Столица")
    print("3 — Уровень дохода")
    print("4 — Регион")
    print("5 — Долгота")
    print("6 — Широта")
    print("0 — Завершить выбор")

    choice = input(
        "\nВведите номера полей через запятую: "
    ).strip()

    if not choice:
        print("Вы ничего не выбрали.")
        return

    selected_fields = choice.split(",")

    print("\n===== ВЫБРАННЫЕ ДАННЫЕ =====")

    for number in selected_fields:
        number = number.strip()

        if number == "0":
            break

        if number in fields:
            field_name, value = fields[number]

            print(
                f"{field_name}: "
                f"{value if value else 'Не указано'}"
            )

        else:
            print(f"Нет поля с номером {number}")


def make_get_country_request():
    """Получает информацию о выбранной стране."""

    country_name = input(
        "Введите название страны на английском: "
    ).strip()

    if not country_name:
        print("Название страны не может быть пустым.")
        return

    country_code = get_country_code(country_name)

    if not country_code:
        print("Страна не найдена. Проверьте название.")
        return

    url = (
        f"https://api.worldbank.org/v2/country/"
        f"{country_code}?format=json"
    )

    print("\nURL запроса:", url)

    try:
        response = requests.get(
            url,
            timeout=15
        )

        result = print_response(response)

        if response.ok and result is not None:
            select_country_fields(result)

    except requests.exceptions.RequestException as error:
        print("Ошибка GET country:", error)


def make_get_request():
    """Отправляет GET-запрос по введённому URL."""

    url = input("Введите URL: ").strip()

    if not url:
        print("URL не может быть пустым.")
        return

    params_input = input(
        "Введите параметры (key=value,key2=value2) "
        "или нажмите Enter: "
    ).strip()

    params = {}

    if params_input:
        try:
            params = dict(
                item.split("=", 1)
                for item in params_input.split(",")
            )

        except ValueError:
            print("Неверный формат параметров.")
            return

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        print_response(response)

    except requests.exceptions.RequestException as error:
        print("Ошибка GET-запроса:", error)


def make_post_request():
    """Отправляет POST-запрос."""

    url = input("Введите URL для POST-запроса: ").strip()

    if not url:
        print("URL не может быть пустым.")
        return

    data_type = input(
        "Отправить данные как JSON? (y/n): "
    ).strip().lower()

    if data_type not in ("y", "n"):
        print("Введите y или n.")
        return

    data_input = input(
        "Введите данные (key=value,key2=value2): "
    ).strip()

    data = {}

    if data_input:
        try:
            data = dict(
                item.split("=", 1)
                for item in data_input.split(",")
            )

        except ValueError:
            print("Неверный формат данных.")
            return

    try:
        if data_type == "y":
            response = requests.post(
                url,
                json=data,
                timeout=15
            )

        else:
            response = requests.post(
                url,
                data=data,
                timeout=15
            )

        print_response(response)

    except requests.exceptions.RequestException as error:
        print("Ошибка POST-запроса:", error)


def main():
    """Главное меню программы."""

    while True:

        print("\n===== ТЕСТИРОВАНИЕ API =====")
        print("1 — GET (выбрать страну)")
        print("2 — GET (ввести URL вручную)")
        print("3 — POST")
        print("0 — Выход")

        choice = input("\nВыберите запрос: ").strip()

        if choice == "1":
            make_get_country_request()

        elif choice == "2":
            make_get_request()

        elif choice == "3":
            make_post_request()

        elif choice == "0":
            print("Программа завершена.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
