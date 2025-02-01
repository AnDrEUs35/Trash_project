from . import parser  
import json

def run(data, output_path, front):
    try:
        with open(front, "r") as file:
            config = json.load(file)

        pars = parser.Parser(data, output_path, config)

        pars.filter_and_save_by_config()

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
    run(data= "./test/data.json", output_path="./test/result_solv_data", front = "./frontend_output.json")