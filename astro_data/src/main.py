import json
from . import parser  # Импортируем модуль parser

def run(config_path):
    try:
        # Чтение конфигурации из frontend_output.json
        with open(config_path, "r") as file:
            config = json.load(file)

        output_path = './astro_data/data_output'  # Установите значение output_path здесь
        
        active_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
        active_satellites = parser.TLEFetch.get_tle_data(active_url)

        # Мусор
        debris_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=fengyun-1c-debris&FORMAT=tle"
        debris_satellites = parser.TLEFetch.get_tle_data(debris_url)



        # Получение времени из frontend_output.json
        # Здесь вы можете добавить логику для получения времени, если это необходимо

        # Обработка спутников и мусора с использованием пользовательского времени
        processor = parser.SatelliteProcess()
        processor.process_satellite(active_satellites)
        processor.process_trash(debris_satellites)
        processor.save()
        # Парсинг frontend_output.json
        pars = parser.Parser("./astro_data/data_output/data.json", output_path, config_path)
        pars.parse_frontend_output()  # Убедитесь, что метод вызывается

        return 'astro_data/data_output/data.json'

    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        return
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
        return
    except Exception as e:
        print(f"Ошибка: {e}")
        return

if __name__ == "__main__":
    run(config_path="./front_output.json")