import requests
from config import WEATHER_API_KEY


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        print(f"Requesting URL: {url}")  # Отладочный вывод
        response = requests.get(url, headers=headers, timeout=20)  # Увеличиваем время ожидания до 20 секунд
        print(f"Response Status Code: {response.status_code}")  # Отладочный вывод
        response.raise_for_status()  # Проверка на успешный статус ответа (код 200)
        data = response.json()
        print(f"Response JSON: {data}")  # Отладочный вывод

        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        city_name = data['name']
        country = data['sys']['country']

        return f"Погода в {city_name}, {country}:\nТемпература: {temperature}°C\nОписание: {weather_description}"

    except requests.exceptions.Timeout:
        return "Запрос к серверу занял слишком много времени. Попробуйте снова."
    except requests.exceptions.HTTPError as errh:
        return f"HTTP ошибка: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Ошибка соединения: {errc}"
    except requests.exceptions.RequestException as err:
        return f"Произошла ошибка при запросе: {err}"


if __name__ == "__main__":
    city = "Moscow"  # Пример города
    weather_info = get_weather(city)
    print(weather_info)  # Отобразите результат в консоли
