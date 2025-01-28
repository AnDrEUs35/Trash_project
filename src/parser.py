import requests
import json
import h5py
from sgp4.api import Satrec
from astropy.time import Time
import sys
from banner import run

run()

class GetData:
    # Функция для получения TLE данных
    def get_tle_data(url):
        response = requests.get(url)
        if response.status_code == 200:
            tle_data = response.text.splitlines()
            satellites = []

            # Проверка на кратность 3
            if len(tle_data) % 3 != 0:
                print("Количество строк не кратно 3")

            for i in range(0, len(tle_data) - 2, 3):
                if i + 2 < len(tle_data):
                    satellite = {
                        "name": tle_data[i].strip(),
                        "line1": tle_data[i + 1].strip(),
                        "line2": tle_data[i + 2].strip()
                    }
                    satellites.append(satellite)
                else:
                    print(f"Пропущена строка {i}, Причина: недостаток данных")
            return satellites
        else:
            print("Ошибка при получении данных")
            sys.exit()

# Спутники
active_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
active_satellites = GetData.get_tle_data(active_url)

# Мусор
debris_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=fengyun-1c-debris&FORMAT=tle"
debris_satellites = GetData.get_tle_data(debris_url)

# Проверка полученных данных о мусоре
if not debris_satellites:
    print("Нет данных о мусоре.")
else:
    print(f"Получено {len(debris_satellites)} спутников мусора.")

# Структура для хранения данных
data = {
    "satellites": [],
    "trash": [],
    "user_properties": {
        "time": 20,
        "time_step": 4,
    }
}

count = 0

# Обработка активных спутников
for satellite in active_satellites:
    line1 = satellite['line1']
    line2 = satellite['line2']
    
    satrec = Satrec.twoline2rv(line1, line2)

    t = Time.now() 
    error_code, teme_p, teme_v = satrec.sgp4(t.jd1, t.jd2)  # в км и км/с

    data["satellites"].append({
        "name": satellite['name'],
        "coords": list(teme_p),  # Преобразуем в список
        "velocity": list(teme_v)  # Преобразуем в список
    })

    count += 1

# Обработка данных о мусоре
for index, satellite in enumerate(debris_satellites, start=1):
    line1 = satellite['line1']
    line2 = satellite['line2']
    
    satrec = Satrec.twoline2rv(line1, line2)

    t = Time.now() 
    error_code, teme_p, teme_v = satrec.sgp4(t.jd1, t.jd2)  # в км и км/с

    data["trash"].append({
        "index": index,
        "coords": list(teme_p),  # Преобразуем в список
        "velocity": list(teme_v)  # Преобразуем в список
    })

# Сохранение данных в JSON файл
with open('data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Все данные успешно сохранены")

print(count)