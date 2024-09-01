import requests


def check_weather_token(api_key: str) -> bool:
    """
    Проверяет работоспособность токена для сайта погоды,
    делая тестовый запрос.

    Args:
        api_key (str): API ключ для сайта погоды.

    Returns:
        bool: True, если токен рабочий, False иначе.
    """

    # Замените на базовый URL вашего API погоды
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    city_name = "Moscow"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)

    if response.status_code == 200:
        print("Токен рабочий")
        return True
    else:
        print("Ошибка! Код:", response.status_code)
        return False


# Введите ваш API ключ
api_key = "fb84801abe556d0fa5a829305ddd718d"

check_weather_token(api_key)