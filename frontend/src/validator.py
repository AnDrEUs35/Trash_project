import json
import datetime


class Validator:
    def __init__(self, data):
        self.data_path = data
        with open(data) as data_file:
            self.data = json.load(data_file) # Чтение данных из файла при создании объекта класса 
            print("  - Данные успешно прочитаны валидатором. Начинаем проверку")

    def date_examination(self):
        self.date = self.data["main_settings"]["DATE"]["value"]
        date_ex = self.date.split('.')
        print(date_ex)
        if self.date == "" or len(date_ex) != 3:
            print(f'  - Ошибка значения в дате: "{self.date}". Должно быть 3 числа через точку.')
            raise ValueError
        else:
            day, month, year = date_ex[0], date_ex[1], date_ex[2]
            for i in date_ex:
                if self.__is_number(i) == False:
                    print(f'  - Ошибка значения в дате: "{self.date}". Значения должны быть целыми числами.')
                    raise ValueError
            else:
                day, month, year = int(day), int(month), int(year)
                self.future_date = datetime.datetime(year, month, day)
                self.date = self.future_date.date()
                
                self.now = datetime.datetime.now()
                self.now = self.now.replace(hour=self.now.hour + 1, minute=0, second=0, microsecond=0)
                print(self.now)

                if day > 31 and (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                    print(f'  - Ошибка значения в дате: "{self.date}". Дней в месяце 31.')
                    raise ValueError
                elif day > 30 and (month == 2 or month == 4 or month == 6 or month == 9 or month == 11):
                    print(f'  - Ошибка значения в дате: "{self.date}". Дней в месяце 30.')
                    raise ValueError
                elif day >= 29 and (month == 2 and (year % 4 != 0 or (year % 100 == 0 and year % 4 == 0))):
                    print(f'  - Ошибка значения в дате: "{self.date}". Дней в феврале 28 или 29 в зависимости от года.')
                    raise ValueError
                elif month < 1 or month > 12:
                    print(f'  - Ошибка значения в дате: "{self.date}". Всего 12 месяцев. Нет нулевого дня месяца.')
                    raise ValueError
                elif day < 1:
                     print(f'  - Ошибка значения в дате: "{self.date}". Месяц начинается с первого дня.')
                     raise ValueError
                elif self.date < self.now.date():
                    print(f'  - Ошибка значения в дате: "{self.date}". Мы не можем моделировать прошлое.')
                    raise ValueError
                else:
                    print('  - Проверка корректности даты прошла успешно.')

    def model_time_examination(self):
        model_time = self.data["main_settings"]["MODEL_TIME"]["value"]
        if model_time == "" or len(model_time) != 5:
            print(f'  - Ошибка значения во временном промежутке: "{model_time}".')
            raise ValueError
        else:
            hour1, hour2 = model_time.split('-')[0], model_time.split('-')[1]
            if self.__is_number(hour1) == False or self.__is_number(hour2) == False:
                print(f'  - Ошибка значения во временном промежутке: "{model_time}". Значения не являются числами')
                raise ValueError
            else:
                hour1, hour2 = int(hour1), int(hour2)

                self.hour_now = self.now.hour

                if (hour1 > 23 or hour1 < 0) or (hour2 > 23 or hour2 < 0):
                    print(f'  - Ошибка значения во временном промежутке: "{model_time}". В сутках 24 часа.')
                    raise ValueError
                elif not 1 <= (hour2 - hour1) % 24 <= 5: 
                    print(f'  - Ошибка значения во временном промежутке: "{model_time}". Промежуток не менее 1 часа, но и не более 5 часов.')
                    raise ValueError
                elif hour1 < self.now.hour and self.date == self.now.date():
                    print(f'  - Ошибка значения во временном промежутке: "{model_time}". Мы не моделируем прошлое. Укажите как минимум начало следующего часа от настоящего момента')
                    raise ValueError
                else:
                    print("  - Проверка выбранного промежутка времени прошла успешно.")
        
    def name_examination(self):
        name = self.data["graf_settings"]["GRAPHIC_NAME"]["value"]
        if name=='':
            print(f'  - Ошибка в значении имени файла: "{name}"')
            raise ValueError
        else:
            print("  - Проверка подписи графика пройдена")

    def __is_number(self, a):
        try:
            int(a)
            return True
        except Exception:
            return False
        
    def counting_time(self):
        time1 = int(self.data['main_settings']['MODEL_TIME']['value'].split('-')[0])
        time2 = int(self.data['main_settings']['MODEL_TIME']['value'].split('-')[1])
        duration = time2 - time1
        count_hours = int(int((self.future_date - self.now).total_seconds()) / 3600 + time1)
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
    validator = Validator(data='test/frontend_output.json')
    validator.date_examination()
    validator.model_time_examination()
    # validator.counting_time()
