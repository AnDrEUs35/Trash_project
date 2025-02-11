import json

class Validator:
    def __init__(self, data):
        with open(data) as data_file:
            self.data = json.load(data_file) # Чтение данных из файла при создании объекта класса 
    
    def date_examination(self):
        date = self.data["time"]["DATE"]["value"]
        if date == "" or len(date.split('.')) != 3:
            print(f'Ошибка значения в "{date}"')
            raise ValueError
        else:
            day, month, year = date.split('.')[0], date.split('.')[1], date.split('.')[2]
            if self.__is_number(day) == False or self.__is_number(month) == False or self.__is_number(year) == False:
                print(f'Ошибка значения в "{date}"')
                raise ValueError
            else:
                day, month, year = int(day), int(month), int(year)
                
                if day > 31 and (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                    print(f'Ошибка значения в "{date}"')
                    raise ValueError
                elif day > 30 and (month == 2 or month == 4 or month == 6 or month == 9 or month == 11):
                    print(f'Ошибка значения в "{date}"')
                    raise ValueError
                elif day > 28 and (month == 2 and (year % 4 != 0 or (year % 100 == 0 and year % 4 == 0))):
                    print(f'Ошибка значения в "{date}"')
                    raise ValueError
                elif month < 1 or month > 12 or day < 1:
                    print(f'Ошибка значения в "{date}"')
                    raise ValueError


    def start_time_examination(self):
        start_time = self.data["time"]["START_TIME"]["value"]
        if start_time == "" or len(start_time.split('.')) != 3:
            print(f'Ошибка значения в "{start_time}"')
            raise ValueError
        else:
            hour, minute, second = start_time.split('.')[0], start_time.split('.')[1], start_time.split('.')[2]
            if self.__is_number(hour) == False or self.__is_number(minute) == False or self.__is_number(second) == False:
                print(f'Ошибка значения в "{start_time}"')
                raise ValueError
            else:
                hour, minute, second = int(hour), int(minute), int(second)
                if (hour > 23 or hour < 0) or (minute > 59 or minute < 0) or (second > 59 or second < 0):
                    print(f'Ошибка значения в "{start_time}"')
                    raise ValueError
        
    def name_examination(self):
        name = self.data["graf_settings"]["FILE_NAME"]["value"]
        if len(name) < 4:
            print(f'Ошибка в значении "{name}"')
            raise ValueError

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
    validator.name_examination()
    