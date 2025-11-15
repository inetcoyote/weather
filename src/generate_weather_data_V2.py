from datetime import datetime, timedelta
import random

# База данных: климат по городам (средние диапазоны температур по сезонам)
MONTHLY_CLIMATE_DATA = {
    "Москва": {
        1:  {"min": -20, "max": -5,  "snow_prob": 0.7, "rain_prob": 0.1},
        2:  {"min": -18, "max": -3,  "snow_prob": 0.6, "rain_prob": 0.2},
        3:  {"min": -8,  "max": 5,   "snow_prob": 0.3, "rain_prob": 0.3},
        4:  {"min": 2,   "max": 15,  "snow_prob": 0.1, "rain_prob": 0.4},
        5:  {"min": 8,   "max": 20,  "snow_prob": 0.0, "rain_prob": 0.4},
        6:  {"min": 12,  "max": 25,  "snow_prob": 0.0, "rain_prob": 0.6},
        7:  {"min": 15,  "max": 28,  "snow_prob": 0.0, "rain_prob": 0.5},
        8:  {"min": 14,  "max": 27,  "snow_prob": 0.0, "rain_prob": 0.5},
        9:  {"min": 8,   "max": 18,  "snow_prob": 0.0, "rain_prob": 0.6},
        10: {"min": 2,   "max": 12,  "snow_prob": 0.1, "rain_prob": 0.7},
        11: {"min": -5,  "max": 5,   "snow_prob": 0.4, "rain_prob": 0.6},
        12: {"min": -15, "max": -3,  "snow_prob": 0.7, "rain_prob": 0.3},
    },
    "Сочи": {
        1:  {"min": 5,  "max": 10, "snow_prob": 0.0, "rain_prob": 0.7},
        2:  {"min": 5,  "max": 11, "snow_prob": 0.0, "rain_prob": 0.6},
        3:  {"min": 6,  "max": 13, "snow_prob": 0.0, "rain_prob": 0.5},
        4:  {"min": 10, "max": 18, "snow_prob": 0.0, "rain_prob": 0.4},
        5:  {"min": 14, "max": 22, "snow_prob": 0.0, "rain_prob": 0.3},
        6:  {"min": 18, "max": 26, "snow_prob": 0.0, "rain_prob": 0.2},
        7:  {"min": 20, "max": 30, "snow_prob": 0.0, "rain_prob": 0.2},
        8:  {"min": 20, "max": 31, "snow_prob": 0.0, "rain_prob": 0.3},
        9:  {"min": 18, "max": 27, "snow_prob": 0.0, "rain_prob": 0.5},
        10: {"min": 13, "max": 22, "snow_prob": 0.0, "rain_prob": 0.7},
        11: {"min": 9,  "max": 16, "snow_prob": 0.0, "rain_prob": 0.8},
        12: {"min": 6,  "max": 11, "snow_prob": 0.0, "rain_prob": 0.8},
    },
    "Новосибирск": {
        1:  {"min": -35, "max": -18, "snow_prob": 0.9, "rain_prob": 0.0},
        2:  {"min": -32, "max": -15, "snow_prob": 0.8, "rain_prob": 0.0},
        3:  {"min": -20, "max": -5,  "snow_prob": 0.6, "rain_prob": 0.1},
        4:  {"min": -5,  "max": 10,  "snow_prob": 0.3, "rain_prob": 0.3},
        5:  {"min": 5,   "max": 18,  "snow_prob": 0.0, "rain_prob": 0.4},
        6:  {"min": 10,  "max": 25,  "snow_prob": 0.0, "rain_prob": 0.5},
        7:  {"min": 13,  "max": 30,  "snow_prob": 0.0, "rain_prob": 0.5},
        8:  {"min": 12,  "max": 28,  "snow_prob": 0.0, "rain_prob": 0.5},
        9:  {"min": 5,   "max": 18,  "snow_prob": 0.1, "rain_prob": 0.5},
        10: {"min": -5,  "max": 10,  "snow_prob": 0.3, "rain_prob": 0.6},
        11: {"min": -15, "max": -2,  "snow_prob": 0.7, "rain_prob": 0.4},
        12: {"min": -30, "max": -10, "snow_prob": 0.9, "rain_prob": 0.1},
    },
    "Мурманск": {
        1:  {"min": -15, "max": -5, "snow_prob": 0.8, "rain_prob": 0.1},
        2:  {"min": -14, "max": -4, "snow_prob": 0.7, "rain_prob": 0.1},
        3:  {"min": -12, "max": -1, "snow_prob": 0.6, "rain_prob": 0.2},
        4:  {"min": -8,  "max": 4,  "snow_prob": 0.5, "rain_prob": 0.2},
        5:  {"min": -3,  "max": 8,  "snow_prob": 0.2, "rain_prob": 0.3},
        6:  {"min": 3,   "max": 14, "snow_prob": 0.0, "rain_prob": 0.5},
        7:  {"min": 8,   "max": 18, "snow_prob": 0.0, "rain_prob": 0.6},
        8:  {"min": 7,   "max": 17, "snow_prob": 0.0, "rain_prob": 0.6},
        9:  {"min": 3,   "max": 12, "snow_prob": 0.1, "rain_prob": 0.6},
        10: {"min": -2,  "max": 6,  "snow_prob": 0.4, "rain_prob": 0.7},
        11: {"min": -8,  "max": 1,  "snow_prob": 0.7, "rain_prob": 0.5},
        12: {"min": -13, "max": -3, "snow_prob": 0.8, "rain_prob": 0.3},
    }
}

# === 2. ПОГОДНЫЕ ОПИСАНИЯ И ОСАДКИ ===
WEATHER_DESC = {
    "снег": {"precip_min": 1.0, "precip_max": 15.0},
    "дождь": {"precip_min": 1.5, "precip_max": 20.0},
    "пасмурно": {"precip_min": 0.0, "precip_max": 1.0},
    "облачно": {"precip_min": 0.0, "precip_max": 0.5},
    "ясно": {"precip_min": 0.0, "precip_max": 0.1},
}

def choose_weather(snow_prob, rain_prob):
    """
    Выбирает тип погоды на основе вероятностей снега и дождя.
    """
    r = random.random()
    if r < snow_prob:
        return "снег"
    elif r < snow_prob + rain_prob:
        return "дождь"
    else:
        # Остальные: ясно, облачно, пасмурно
        return random.choices(
            ["ясно", "облачно", "пасмурно"],
            weights=[0.4, 0.3, 0.3]
        )[0]


def get_climate_for_date(city, date):
    """
    Возвращает климатические параметры для конкретной даты (по месяцу).
    """
    month = date.month
    if city not in MONTHLY_CLIMATE_DATA:
        raise ValueError(f"Город {city} не поддерживается.")
    return MONTHLY_CLIMATE_DATA[city][month]


def generate_realistic_weather(city="Москва", days=90):
    """
    Генерирует реалистичный прогноз погоды на заданное количество дней.
    Учитывает месячные температурные ограничения.
    """
    today = datetime.today()
    data = []

    for i in range(days):
        current_date = today + timedelta(days=i)
        year, month, day = current_date.year, current_date.month, current_date.day

        # Получаем климатические параметры для этого месяца
        climate = get_climate_for_date(city, current_date)
        base_min = climate["min"]
        base_max = climate["max"]
        snow_prob = climate["snow_prob"]
        rain_prob = climate["rain_prob"]

        # Выбираем тип погоды
        weather_type = choose_weather(snow_prob, rain_prob)
        desc = WEATHER_DESC[weather_type]

        # Генерируем среднюю температуру в рамках месячного диапазона
        avg_temp = round(random.uniform(base_min, base_max), 1)

        # Минимальная и максимальная температура с небольшим разбросом
        temp_range = random.uniform(4.0, 8.0)  # суточный разброс
        min_temp = int(round(avg_temp - temp_range * random.uniform(0.4, 0.6), 1))
        max_temp = int(round(avg_temp + temp_range * random.uniform(0.4, 0.6), 1))

        # Подстраховка: min ≤ avg ≤ max
        avg_temp = int(round((min_temp + max_temp) / 2, 1))

        # Осадки
        if weather_type in ["снег", "дождь"]:
            precipitation = round(random.uniform(desc["precip_min"], desc["precip_max"]), 1)
        else:
            precipitation = 0.0

        # Добавляем строку данных
        new_row = [year, month, day, min_temp, max_temp, avg_temp, precipitation, weather_type]
        data.append(new_row)

    return data


# === 3. ГЕНЕРАЦИЯ И ВЫВОД ДАННЫХ ===
city = "Москва"  # ← измените на нужный город: "Сочи", "Новосибирск", "Мурманск"

# Генерация прогноза на 90 дней
forecast = generate_realistic_weather(city, days=90)

# Вывод первых 7 строк
print(f"Прогноз погоды на 7 дней вперёд для {city}:\n")
for row in forecast[:7]:
    print(f"{row[2]:02d}.{row[1]:02d}.{row[0]} | "
          f"Мин: {row[3]}°C, Макс: {row[4]}°C, Сред: {row[5]}°C, "
          f"Осадки: {row[6]} мм, Погода: {row[7]}")

# === 4. СОХРАНЕНИЕ В CSV ===
import csv

with open('weather_forecast.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    # Заголовки на английском (для универсальности)
    writer.writerow([
        'year', 'month', 'day',
        'temperature_min', 'temperature_max', 'temperature_avg',
        'precipitation_mm', 'condition'
    ])
    writer.writerows(forecast)

print("\n✅ Прогноз успешно сохранён в 'weather_forecast.csv'")