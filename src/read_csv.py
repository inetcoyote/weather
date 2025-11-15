import pandas as pd
import csv
import random
from datetime import datetime, timedelta


# Основная функция
def main():
    #CSV_read()
    #CSV_generate()
    CSV_week()

def CSV_read():
    # URL к raw-версии CSV-файла на GitHub
    #url = 'https://raw.githubusercontent.com/inetcoyote/weather/refs/heads/main/weather.csv'
    # Чтение CSV-файла
    #df = pd.read_csv(url, sep=';')

    # Укажите путь к вашему CSV-файлу
    file_path = 'weather.csv'  # если файл лежит в корне проекта
    # Чтение CSV
    df = pd.read_csv(file_path, sep=';')

    # Вывод первых нескольких строк
    print(df)

def CSV_generate():

    # Данные для добавления (например, новая строка)
    #new_row = ['Иван', 25, 'Москва']
    new_row = [2025,11,24,-6,-6,-2,2.1,"снег"]

    # Открываем файл в режиме 'a' (append — добавление)
    with open('weather.csv', mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_row)

    print("Данные успешно добавлены в CSV.")

def CSV_week():

    # Возможные погодные условия и их параметры
    weather_types = [
        {"desc": "снег", "min": -15, "max": 0, "precip_min": 1.0, "precip_max": 10.0},
        {"desc": "дождь", "min": 0, "max": 15, "precip_min": 1.5, "precip_max": 12.0},
        {"desc": "пасмурно", "min": -5, "max": 10, "precip_min": 0.0, "precip_max": 1.0},
        {"desc": "облачно", "min": -8, "max": 12, "precip_min": 0.0, "precip_max": 0.5},
        {"desc": "ясно", "min": -10, "max": 20, "precip_min": 0.0, "precip_max": 0.1},
    ]

    def generate_weather():
        weather = random.choice(weather_types)
        avg_temp = round(random.uniform(weather["min"], weather["max"]), 1)
        min_temp = round(avg_temp - random.uniform(0, 5), 1)
        max_temp = round(avg_temp + random.uniform(0, 5), 1)
        precipitation = round(random.uniform(weather["precip_min"], weather["precip_max"]), 1)
        return [min_temp, max_temp, avg_temp, precipitation, weather["desc"]]

    # Генерация данных на 7 дней вперёд
    start_date = datetime.today()
    data = []

    for i in range(7):
        current_date = start_date + timedelta(days=i)
        year, month, day = current_date.year, current_date.month, current_date.day
        min_t, max_t, avg_t, precip, weather = generate_weather()
        new_row = [year, month, day, min_t, max_t, avg_t, precip, weather]
        data.append(new_row)

    # Вывод результата
    for row in data:
        print(row)


if __name__ == '__main__':
    main()