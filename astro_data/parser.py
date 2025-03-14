import requests
import json
from sgp4.api import Satrec
from astropy.time import Time
import sys
import os 
from datetime import datetime

class Satellite:
    def __init__(self, name, line1, line2):
        self.name = name
        self.line1 = line1
        self.line2 = line2
        self.coords = None
        self.velocity = None

    def calculate_pos(self, custom_time=None):
        satrec = Satrec.twoline2rv(self.line1, self.line2)
        if custom_time:
            t = Time(custom_time)  # Используем пользовательское время
        else:
            t = Time.now()  # Используем текущее время, если custom_time не указано
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

    def process_satellite(self, satellites, custom_time=None):
        for satellite in satellites:
            satellite.calculate_pos()
            self.data["satellites"].append({
                "name": satellite.name,
                "coords": satellite.coords,  
                "velocity": satellite.velocity  
            })

    def process_trash(self, trash, custom_time=None):
        for index, satellite in enumerate(trash, start=1):
            satellite.calculate_pos()
            self.data["trash"].append({
                "index": index,
                "coords": satellite.coords, 
                "velocity": satellite.velocity 
            })

    def save(self, file_name='data.json'):
        output_path = './astro_data/data_output/' + file_name  # Указываем путь для сохранения
        with open(output_path, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)
        print(f"Все данные успешно сохранены в {output_path}")


class Parser:
    def __init__(self, data, output_path, config_path):
        self.data = data
        self.output_path = output_path
        self.config_path = config_path

    def parse_frontend_output(self):
        try:
            # Чтение данных из frontend_output.json
            with open(self.config_path, 'r') as frontend_file:
                frontend_data = json.load(frontend_file)

            # Чтение существующих данных из data.json (если файл существует)
            if os.path.exists(self.data):
                with open(self.data, 'r') as data_file:
                    existing_data = json.load(data_file)
            else:
                existing_data = {
                    "satellites": [],
                    "trash": [],
                    "user_properties": {
                        "time": 20,
                        "time_step": 4,
                    }
                }

            # Добавление данных из frontend_output.json в существующие данные
            if isinstance(frontend_data, dict) and isinstance(existing_data, dict):
                if "objects" in frontend_data:
                    for item in frontend_data["objects"]:
                        if item.get("type") == "satellite":
                            existing_data["satellites"].append({
                                "name": item.get("name"),
                                "coords": item.get("coordinates"),
                                "velocity": item.get("velocity"),
                            })
                        elif item.get("type") == "trash":
                            existing_data["trash"].append({
                                "index": len(existing_data["trash"]) + 1,
                                "coords": item.get("coordinates"),
                                "velocity": item.get("velocity"),
                            })
                else:
                    # Если frontend_data не содержит "objects", просто объединяем словари
                    existing_data.update(frontend_data)

            # Сохранение обновленных данных в data.json
            with open(self.data, 'w') as data_file:
                json.dump(existing_data, data_file, indent=4)
            print(f"Данные из frontend_output.json успешно добавлены в {self.data}")
        except FileNotFoundError:
            print("Файл frontend_output.json не найден.")
        except json.JSONDecodeError:
            print("Ошибка при чтении JSON из frontend_output.json.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

def main():
    # Спутники
    active_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
    active_satellites = TLEFetch.get_tle_data(active_url)

    # Мусор
    debris_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=fengyun-1c-debris&FORMAT=tle"
    debris_satellites = TLEFetch.get_tle_data(debris_url)

    

    # Получение времени из frontend_output.json
    # Здесь вы можете добавить логику для получения времени, если это необходимо

    # Обработка спутников и мусора с использованием пользовательского времени
    processor = SatelliteProcess()
    processor.process_satellite(active_satellites)
    processor.process_trash(debris_satellites)
    processor.save()
    # Парсинг frontend_output.json
    parser = Parser(data='./astro_data/data_output/data.json', output_path='output')
    parser.parse_frontend_output()  # Убедитесь, что метод вызывается
    print("Все данные были успешно записаны")

if __name__ == "__main__":
    main()