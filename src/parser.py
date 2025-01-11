import requests
import json
import h5py
from sgp4.api import Satrec
from astropy.time import Time

# Получение TLE данных
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
response = requests.get(url)

if response.status_code == 200:
    tle_data = response.text.splitlines()
    satellites = []

    for i in range(0, len(tle_data), 3):
        satellite = {
            "name": tle_data[i].strip(),
            "line1": tle_data[i + 1].strip(),
            "line2": tle_data[i + 2].strip()
        }
        satellites.append(satellite)

    print("Данные успешно получены.")
else:
    print("Ошибка при получении данных")
    sys.exit()

# Создание HDF5 файла для записи данных
with h5py.File('satellites.hdf5', 'w') as hdf:
    for satellite in satellites:
        # Получение скорости для каждого спутника
        line1 = satellite['line1']
        line2 = satellite['line2']
        
        # Создание объекта спутника
        satrec = Satrec.twoline2rv(line1, line2)

        # Используем текущее время для вычисления положения и скорости
        t = Time.now()  # Текущее время
        error_code, teme_p, teme_v = satrec.sgp4(t.jd1, t.jd2)  # в км и км/с

        # Запись данных в HDF5 файл
        group = hdf.create_group(satellite['name'])
        group.create_dataset('position', data=teme_p)
        group.create_dataset('velocity', data=teme_v)

        print(f"Данные для {satellite['name']} успешно записаны в HDF5 файл.")

print("Все данные успешно сохранены в satellites.h5")