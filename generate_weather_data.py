from datetime import datetime, timedelta
import random

# База данных: климат по городам (средние диапазоны температур по сезонам)
CLIMATE_DATA = {
    "Москва": {
        "зима":   {"min": -20, "max": -5, "snow_prob": 0.7, "rain_prob": 0.2},
        "весна":  {"min": -5,  "max": 15, "snow_prob": 0.1, "rain_prob": 0.5},
        "лето":   {"min": 12,  "max": 28, "snow_prob": 0.0, "rain_prob": 0.6},
        "осень":  {"min": -3,  "max": 15, "snow_prob": 0.3, "rain_prob": 0.6},
    },
    "Сочи": {
        "зима":   {"min": 5,   "max": 12, "snow_prob": 0.0, "rain_prob": 0.8},
        "весна":  {"min": 8,   "max": 20, "snow_prob": 0.0, "rain_prob": 0.5},
        "лето":   {"min": 20,  "max": 32, "snow_prob": 0.0, "rain_prob": 0.3},
        "осень":  {"min": 12,  "max": 22, "snow_prob": 0.0, "rain_prob": 0.7},
    },
    "Новосибирск": {
        "зима":   {"min": -35, "max": -15, "snow_prob": 0.9, "rain_prob": 0.05},
        "весна":  {"min": -10, "max": 15, "snow_prob": 0.3, "rain_prob": 0.5},
        "лето":   {"min": 10,  "max": 30, "snow_prob": 0.0, "rain_prob": 0.6},
        "осень":  {"min": -15, "max": 10, "snow_prob": 0.4, "rain_prob": 0.5},
    },
    "Мурманск": {
        "зима":   {"min": -15, "max": -5, "snow_prob": 0.8, "rain_prob": 0.1},
        "весна":  {"min": -8,  "max": 5,  "snow_prob": 0.5, "rain_prob": 0.3},
        "лето":   {"min": 5,   "max": 18, "snow_prob": 0.0, "rain_prob": 0.6},
        "осень":  {"min": -10, "max": 3,  "snow_prob": 0.7, "rain_prob": 0.5},
    }
}

# Погодные описания
WEATHER_DESC = {
    "снег": {"precip_min": 1.0, "precip_max": 15.0},
    "дождь": {"precip_min": 1.5, "precip_max": 20.0},
    "пасмурно": {"precip_min": 0.0, "precip_max": 1.0},
    "облачно": {"precip_min": 0.0, "precip_max": 0.5},
    "ясно": {"precip_min": 0.0, "precip_max": 0.1},
}

def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return "зима"
    elif month in [3, 4, 5]:
        return "весна"
    elif month in [6, 7, 8]:
        return "лето"
    else:
        return "осень"

def choose_weather(snow_prob, rain_prob):
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

def generate_realistic_weather(city="Москва"):
    today = datetime.today()
    season = get_season(today)

    if city not in CLIMATE_DATA:
        raise ValueError(f"Город {city} не поддерживается. Доступные: {list(CLIMATE_DATA.keys())}")

    climate = CLIMATE_DATA[city][season]
    base_min = climate["min"]
    base_max = climate["max"]
    snow_prob = climate["snow_prob"]
    rain_prob = climate["rain_prob"]

    data = []
    for i in range(90):
        current_date = today + timedelta(days=i)
        year, month, day = current_date.year, current_date.month, current_date.day

        # Выбираем тип погоды
        weather_type = choose_weather(snow_prob, rain_prob)
        desc = WEATHER_DESC[weather_type]

        # Генерируем температуру в рамках сезона и города
        avg_temp = round(random.uniform(base_min, base_max), 1)
        min_temp = round(avg_temp - random.uniform(0, 5), 1)
        max_temp = round(avg_temp + random.uniform(0, 5), 1)

        # Осадки
        precipitation = round(random.uniform(desc["precip_min"], desc["precip_max"]), 1) if weather_type in ["снег", "дождь"] else 0.0

        new_row = [year, month, day, min_temp, max_temp, avg_temp, precipitation, weather_type]
        data.append(new_row)

    return data

# === ГЕНЕРАЦИЯ ДАННЫХ ===
city = "Москва"  # ← поменяйте на нужный город
forecast = generate_realistic_weather(city)

# Вывод
print(f"Прогноз погоды на 7 дней вперед для {city}:\n")
for row in forecast:
    print(row)

# Сохранение в CSV (опционально)
import csv
with open('weather_forecast.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    #writer.writerow(['Год', 'Месяц', 'День', 'МинТ', 'МаксТ', 'СредТ', 'Осадки_мм', 'Погода'])
    writer.writerow(['year','month','day','temperature_avg','temperature_max','temperature_min','precipitation_mm','condition'])
    writer.writerows(forecast)

print("\n✅ Данные сохранены в 'weather_forecast.csv'")