from . import parser  
import json

def run(data):
    try:
        parser.main(data)

    except json.JSONDecodeError as e:
        print(f"Ошибка при декода JSON: {e}")
        return
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
        return
    except Exception as e:
        print(f"Ошибка: {e}")
        return
    

if __name__ == "__main__":
    run(data= "./astro_data/test/frontend_output.json")