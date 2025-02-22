from . import validator
import yaml
import datetime

def run_validator(data_path):
    valid = validator.Validator(data_path)
    valid.date_examination()
    valid.start_time_examination()

def change_time(path):
    with open(path, encoding="UTF-8") as f:
        data = yaml.safe_load(f)

    now = datetime.datetime.now().date()
    now = f'{now.day}.{now.month}.{now.year}'

    data['FIELDS']['DATE']['default'] = now
    with open("frontend/src/config.yml", "w", encoding="UTF-8") as f:
        yaml.dump(data, f, allow_unicode=True)
        

if __name__=='__main__':
    #change_time('/workspaces/Trash_project/frontend/src/test.yml')
    run_validator('/workspaces/Trash_project/test/frontend_output.json')
    