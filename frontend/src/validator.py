import json
import datetime

class Validator:
    def __init__(self, data):
        with open(data) as data_file:
            self.data = json.load(data_file) # Чтение данных из файла при создании объекта класса 
            print("Данные успешно прочитаны валидатором. Начинаем проверку")

    def date_examination(self):
        date = self.data["main_settings"]["DATE"]["value"]
        if date == "" or len(date.split('.')) != 3:
            print(f'Ошибка значения в дате: "{date}"')
            raise ValueError
        else:
            day, month, year = date.split('.')[0], date.split('.')[1], date.split('.')[2]
            if self.__is_number(day) == False or self.__is_number(month) == False or self.__is_number(year) == False:
                print(f'Ошибка значения в дате: "{date}"')
                raise ValueError
            else:
                day, month, year = int(day), int(month), int(year)

                date_now = str(datetime.datetime.now().date())
                day_now, month_now, year_now = int(date_now.split('-')[2]), int(date_now.split('-')[1]), int(date_now.split('-')[0])

                self.date_now_for_time = str(day_now) + '.' + str(month_now) + '.' + str(year_now)
                self.date_for_time = str(day) + '.' + str(month) + '.' + str(year)

                if day > 31 and (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                    print(f'Ошибка значения в дате: "{date}"')
                    raise ValueError
                elif day > 30 and (month == 2 or month == 4 or month == 6 or month == 9 or month == 11):
                    print(f'Ошибка значения в дате: "{date}"')
                    raise ValueError
                elif day > 28 and (month == 2 and (year % 4 != 0 or (year % 100 == 0 and year % 4 == 0))):
                    print(f'Ошибка значения в дате: "{date}"')
                    raise ValueError
                elif month < 1 or month > 12 or day < 1:
                    print(f'Ошибка значения в дате: "{date}"')
                    raise ValueError
                elif (day < day_now and month == month_now and year == year_now) or (month < month_now and year == year_now) or year < year_now:
                    print(f'Ошибка значения в дате: "{date}". Мы не можем моделировать прошлое.')
                    raise ValueError
                else:
                    print('Проверка корректности даты прошла успешно.')

    def start_time_examination(self):
        start_time = self.data["main_settings"]["START_TIME"]["value"]
        if start_time == "" or len(start_time.split('.')) != 3:
            print(f'Ошибка значения во времени отсчёта: "{start_time}"')
            raise ValueError
        else:
            hour, minute, second = start_time.split('.')[0], start_time.split('.')[1], start_time.split('.')[2]
            if self.__is_number(hour) == False or self.__is_number(minute) == False or self.__is_number(second) == False:
                print(f'Ошибка значения во времени отсчёта: "{start_time}"')
                raise ValueError
            else:
                hour, minute, second = int(hour), int(minute), int(second)

                time_now = datetime.datetime.now().time()
                hour_now, minute_now, second_now = time_now.hour, time_now.minute, time_now.second

                if (hour > 23 or hour < 0) or (minute > 59 or minute < 0) or (second > 59 or second < 0):
                    print(f'Ошибка значения во времени отсчёта: "{start_time}"')
                    raise ValueError
                elif (hour, minute, second) < (hour_now, minute_now, second_now) and self.date_for_time == self.date_now_for_time:
                    print(f'Ошибка значения во времени отсчёта: "{start_time}". Мы не моделируем прошлое.')
                    raise ValueError
                else:
                    print("Проверка времени отсчёта прошла успешно.")
        
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

if __name__ == '__main__':
    validator = Validator(data='test/frontend_output_bug.json')
    validator.start_time_examination()
    validator.date_examination()

    