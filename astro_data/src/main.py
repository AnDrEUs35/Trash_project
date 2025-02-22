import json
from . import parser  # Импортируем модуль parser

def run(config_path):
    try:
        # Чтение конфигурации из frontend_output.json
        with open(config_path, "r") as file:
            config = json.load(file)

        output_path = './astro_data/data_output'  # Установите значение output_path здесь
        pars = parser.Parser("./astro_data/data_output/data.json", output_path)

        pars.filter_and_save_by_config(config)  # Передаем конфигурацию в метод

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