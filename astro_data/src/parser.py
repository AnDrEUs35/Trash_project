import requests
import json
from sgp4.api import Satrec
from astropy.time import Time
import sys
from . import banner
import os 
from datetime import datetime

class Satellite:
    def __init__(self, name, line1, line2):
        self.name = name
        self.line1 = line1
        self.line2 = line2
        self.coords = None
        self.velocity = None

    def calculate_pos(self):
        satrec = Satrec.twoline2rv(self.line1, self.line2)
        t = Time.now() 
        error_code, teme_p, teme_v = satrec.sgp4(t.jd1, t.jd2)  # в км и км/с
        if error_code == 0:
            self.coords = list(teme_p)
            self.velocity = list(teme_v)
        else:
            print(f"Ошибка при вычислении {self.name}: код ошибки {error_code}")

class TLEFetch:
    @staticmethod
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
                    satellite = Satellite(
                        name=tle_data[i].strip(),
                        line1=tle_data[i + 1].strip(),
                        line2=tle_data[i + 2].strip()
                    )
                    satellites.append(satellite)
                else:
                    print(f"Пропущена строка {i}, Причина: недостаток данных")
            return satellites
        else:
            print("Ошибка при получении данных")
            sys.exit()

class SatelliteProcess:
    def __init__(self):
        self.data = {
            "satellites": [],
            "trash": [],
            "user_properties": {
                "time": 20,
                "time_step": 4,
            }
        }

    def process_satellite(self, satellites):
        for satellite in satellites:
            satellite.calculate_pos()
            self.data["satellites"].append({
                "name": satellite.name,
                "coords": satellite.coords,  
                "velocity": satellite.velocity  
            })

    def process_trash(self, trash):
        for index, satellite in enumerate(trash, start=1):
            satellite.calculate_pos()
            self.data["trash"].append({
                "index": index,
                "coords": satellite.coords, 
                "velocity": satellite.velocity 
            })

    def save(self, file_name='data.json'):
        with open(file_name, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)
        print("Все данные успешно сохранены")


class Parser:
    def __init__(self, data, output_path, config):
        self.data = data
        self.output_path = output_path
        self.config = config

    def filter_and_save_by_config(self):
        # Извлечение параметров из конфигурации
        object_type = self.config['model']['OBJ_TYPE']['value']  # Тип объекта (спутник или мусор)
        current_date_str = self.config['time']['DATE']['value']  # Текущая дата
        current_date = datetime.strptime(current_date_str, "%d.%m.%Y").date()

        # Чтение данных из data.json
        with open(self.data, 'r') as data_file:
            data_content = json.load(data_file)

        if not isinstance(data_content, dict):
            raise ValueError("data.json должен содержать объект.")


        # Фильтрация объектов по типу и дате
        filtered_objects = []
        if object_type == "satellite":
            objects_to_filter = data_content.get("satellites", [])
        elif object_type == "trash":
            objects_to_filter = data_content.get("trash", [])
        else:
            raise ValueError("Неподдерживаемый тип объекта.")
        
        for item in objects_to_filter:
            filtered_objects.append(item)

        # Создание нового JSON с отфильтрованными объектами
        result = {
            "config": self.config,
            "filtered_objects": filtered_objects
        }

        # Сохранение результатов в новый JSON-файл
        os.makedirs(self.output_path, exist_ok=True)  # Создание директории, если её нет
        output_file = f"{self.output_path}/filtered_by_config.json"
        with open(output_file, 'w') as json_file:
            json.dump(result, json_file, indent=4)
        print(f"Отфильтрованные объекты успешно сохранены в {output_file}")

def main():
    # Спутники
    active_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
    active_satellites = TLEFetch.get_tle_data(active_url)

    # Мусор
    debris_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=fengyun-1c-debris&FORMAT=tle"
    debris_satellites = TLEFetch.get_tle_data(debris_url)

    processor = SatelliteProcess()
    processor.process_satellite(active_satellites)
    processor.process_trash(debris_satellites)
    processor.save()

    print("Все данные были успешно записаны")

if __name__ == "__main__":
    banner.run()
    main()