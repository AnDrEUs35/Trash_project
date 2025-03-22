import json
import datetime
from dateutil.parser import parse

class Validator:
    def __init__(self, data):
        self.data_path = data
        with open(data) as data_file:
            self.data = json.load(data_file) # Чтение данных из файла при создании объекта класса 
            print("Данные успешно прочитаны валидатором. Начинаем проверку")

    def date_examination(self):
        self.date = self.data["main_settings"]["DATE"]["value"]
        if self.date == "" or len(self.date.split('.')) != 3:
            print(f'Ошибка значения в дате: "{self.date}"')
            raise ValueError
        else:
            day, month, year = self.date.split('.')[0], self.date.split('.')[1], self.date.split('.')[2]
            if self.__is_number(day) == False or self.__is_number(month) == False or self.__is_number(year) == False:
                print(f'Ошибка значения в дате: "{self.date}"')
                raise ValueError
            else:
                day, month, year = int(day), int(month), int(year)

                date_now = str(datetime.datetime.now().date())
                day_now, month_now, year_now = int(date_now.split('-')[2]), int(date_now.split('-')[1]), int(date_now.split('-')[0])

                self.date_now_for_time = str(day_now) + '.' + str(month_now) + '.' + str(year_now)
                # self.date_for_time = str(day) + '.' + str(month) + '.' + str(year)
                


                if day > 31 and (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                    print(f'Ошибка значения в дате: "{self.date}"')
                    raise ValueError
                elif day > 30 and (month == 2 or month == 4 or month == 6 or month == 9 or month == 11):
                    print(f'Ошибка значения в дате: "{self.date}"')
                    raise ValueError
                elif day > 28 and (month == 2 and (year % 4 != 0 or (year % 100 == 0 and year % 4 == 0))):
                    print(f'Ошибка значения в дате: "{self.date}"')
                    raise ValueError
                elif month < 1 or month > 12 or day < 1:
                    print(f'Ошибка значения в дате: "{self.date}"')
                    raise ValueError
                elif (day < day_now and month == month_now and year == year_now) or (month < month_now and year == year_now) or year < year_now:
                    print(f'Ошибка значения в дате: "{self.date}". Мы не можем моделировать прошлое.')
                    raise ValueError
                else:
                    print('Проверка корректности даты прошла успешно.')

    def model_time_examination(self):
        model_time = self.data["main_settings"]["MODEL_TIME"]["value"]
        if model_time == "" or len(model_time) != 5:
            print(f'Ошибка значения во временном промежутке: "{model_time}".')
            raise ValueError
        else:
            hour1, hour2 = model_time.split('-')[0], model_time.split('-')[1]
            if self.__is_number(hour1) == False or self.__is_number(hour2) == False:
                print(f'Ошибка значения во временном промежутке: "{model_time}". Значения не являются числами')
                raise ValueError
            else:
                hour1, hour2 = int(hour1), int(hour2)

                hour_now = datetime.datetime.now().time().hour

                if (hour1 > 23 or hour1 < 0) or (hour2 > 23 or hour2 < 0):
                    print(f'Ошибка значения во временном промежутке: "{model_time}". В сутках 24 часа.')
                    raise ValueError
                elif hour2 - hour1 > 5 or -19 < hour2 - hour1 < 0 :
                    print(f'Ошибка значения во временном промежутке: "{model_time}". Промежуток не более 5 часов')
                    raise ValueError
                elif hour2 == hour1:
                    print(f'Ошибка значения во временном промежутке: "{model_time}".')
                    raise ValueError
                elif hour1 < hour_now and self.date == self.date_now_for_time:
                    print(f'Ошибка значения во временном промежутке: "{model_time}". Мы не моделируем прошлое.')
                    raise ValueError
                else:
                    print("Проверка выбранного промежутка времени прошла успешно.")
        
    def name_examination(self):
        name = self.data["graf_settings"]["GRAPHIC_NAME"]["value"]
        if name=='':
            print(f'Ошибка в значении имени файла: "{name}"')
            raise ValueError
        else:
            print("Проверка подписи графика пройдена")

    def __is_number(self, a):
        try:
            int(a)
            return True
        except ValueError:
            return False
        
    def counting_time(self):
        # parse преобразует строковое значение даты в объекты datetime
        duration = int(self.data['main_settings']['MODEL_TIME']['value'].split('-')[1]) - int(self.data['main_settings']['MODEL_TIME']['value'].split('-')[0])
        count_hours = (parse(self.date) - parse(self.date_now_for_time)).days * 24
        adding = {
                "max_time": {
                    "value": count_hours + duration
                },
                "snap_start": {
                    "value": count_hours
                }
            }
        self.data['time_for_count'] = adding
        with open(self.data_path, 'w') as data_file:
            json.dump(self.data, data_file, indent=4)  # indent задаёт отсутпы для читабельности
if __name__ == '__main__':
    validator = Validator(data='test/frontend_output_bug.json')
    validator.start_time_examination()
    validator.date_examination()