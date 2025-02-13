# FrontEnd

## Конфигурация
Конфигурационный Yaml-файл содержит поля, которые пользователь должен заполнить, а также их структуру.
Рассмотрим для начала структуру.
```python
STRUCTURE:
    - group:
        key: main_settings
        title:  
            ru: Общие настройки
        fields:
            - separator:
                title:
                  ru: Координаты            
            - field: WIDTH
            - field: LONG
            - field: RADIUS
            - separator:
                title:
                  ru: Время
            - field: DATE
            - field: START_TIME
            - field: DURATION
            - field: STEP
            - separator:
                title:
                  ru: Тип объекта моделирования
            - field: TRASH_TYPE
              width: full
            - field: SATELITE_TYPE
              width: full        
    
    - group:
        key: graf_settings
        title:  
            ru: Настройки графика
        fields:
            - field: FILE_NAME
            - field: COLOR
              view: dropdown
            - field: MARKER_FORM
              view: dropdown
            - field: MARKER_SIZE
            - field: LINE_STYLE
              view: dropdown
            - field: TYPE_OF_FILE

    - group:
        key: user_satelites
        title:
            ru: Добавление спутников
        fields:
            - field: USER_SATELITE
              width: full
```

Как мы видим, структура содержит три группы полей:
- Общие настройки
- Настройки графики
- Добавление спутников

Рассмотрим каждую из них поподробнее.

### Общие настройки
Данная вкладка состоит из нескольких разделов.
Первый из них - 'Координаты'. Здесь пользователь выбирает на карте точку, область вокруг которой, описанную радиусом, мы будем моделировать.
Раздел содержит три поля: широта (от -90 до 90), долгота (от -180 да 180), радиус области (от 1 до 30). Все они задаются целочисленными значениями.
```python
    WIDTH:
        type: integer
        title:
            ru: Широта
        hint:
            ru: Введите широту в градусах, тип данных int
        min: -90
        max: 90
        default: 0

    LONG:
        type: integer
        title:
            ru: Долгота
        hint:
            ru: Введите долготу в градусах, тип данных int
        min: -180
        max: 180
        default: 0

    RADIUS:
        type: integer
        title:
            ru: Радиус области моделирования
        hint:
            ru: Введите радиус выбранной области в градусах, тип данных int
        default: 1
        max: 30
        min: 1
```

В разделе «Время» необходимо задать дату и время начала отсчёта. Значения принимаются в виде трёх чисел, записанных через точку. В связи с тем, что данные из этих двух полей в таком виде, в каком было бы удобно пользователю, можно было принять только как строки, была написана программа, проверяющая правильность ввода (Валидатор, о котором будет сказано ниже). Также здесь в секундах задаются продолжительность моделирования и временной шаг.
```python
    DATE:
        type: string
        title:  
            ru: Дата начала отсчёта
        hint:
            ru: Введите дату в виде дд.мм.гггг; Не используйте буквы
        default: 10.2.2025

    START_TIME:
        type: string
        title:  
            ru: Время начала отсчёта
        hint:
            ru: Введите время в виде чч.мм.сс; Не используйте буквы
        default: 00.00.00
    
    DURATION:
        type: integer
        title:  
            ru: Продолжительность моделирования
        hint:
            ru: Укажите промежуток времени в секундах, тип данных int
        default: 100
        min: 1
    
    STEP:
        type: integer
        hint:
            ru: Укажите временной шаг в секундах для моделирования, тип данных int
        title:
            ru: Шаг моделироввания
        default: 1
```

В разделе «Тип объекта моделирования» выбирается, какие объекты будет моделировать программа. Выбор осуществляется посредством двух флажков, которые могут принимать значения True/False. Один из них отвечает за моделирование спутников, а другой ‒ мусора.
```python
    TRASH_TYPE:
        type: boolean
        hint:
            ru: Выбрав этот пункт, вы получите в результате модель динамики мусора
        title:  
            ru: Мусор
    
    SATELITE_TYPE:
        type: boolean
        hint:
            ru: Выбрав этот пункт, вы получите в результате модель динамики спутников
        title:
            ru: Спутник
```

### Настройки графика
Данная вкладка даёт пользователю возможность настроить под себя файл с результатом моделирования, который он получит в конце. Так, пользователь должен ввести название файла, выбрать из выпадающих списков цвет, форму, стиль линии траектории, а также ввести размер маркера и выбрать тип файла (.png или .gif). Все эти параметры позволяют сделать модель более наглядной.
```python
    FILE_NAME:
        type: string
        title:  
            ru: Имя файла
        hint:
            ru: Введите имя файла
        default: test
    
    COLOR:
        type: string
        title:  
            ru: Цвет маркера
        hint:
            ru: Выберите из выпадающего списка цвет для обозначения маркеров спутников и мусора
        default: 'black'
        enum:
          - value: 'black'
            name:
              ru: Чёрный
          - value: 'red'
            name:
              ru: Красный
          - value: 'blue'
            name:
              ru: Синий
          - value: 'green'
            name:
              ru: Зелёный
          - value: 'yellow'
            name:
              ru: Жёлтый
          - value: 'pink'
            name:
              ru: Розовый  


    MARKER_FORM:
        type: string
        title:  
            ru: Форма маркера
        hint:
            ru: Выберите форму маркера для обозначения на графике спутников и мусора
        default: 'o'
        enum:
            - value: 'o'
              name:
                  ru: Круг
            - value: 's'
              name:
                  ru: Квадрат
            - value: '*'
              name:
                  ru: Звезда
            - value: 'D'
              name:
                  ru: Ромб
            - value: 'x'
              name:
                  ru: X-образный

    MARKER_SIZE:
        type: integer
        title:  
            ru: Размер маркера
        hint:
            ru: Введите число для обозначения размера, int
        default: 5

    LINE_STYLE:
        type: string
        title:  
            ru: Стиль линии
        hint:
            ru: Выберите стиль траекторий, которые будут рисоваться выбранными вами объектами моделирования
        default: '-'
        enum:
            - value: '-'
              name:
                  ru: Сплошная линия
            - value: '--'
              name:
                  ru: Штриховая линия
            - value: '-.'
              name:
                  ru: Штрих-пунктирная линия
            - value: ':'
              name:
                  ru: Пунктирная линия

    # выпадающий список
    TYPE_OF_FILE:
        type: string
        title:  
            ru: Тип файла
        hint:
            ru: Выберите подходящее под ваши цели расширение файла
        enum:
            - value: '.png'
              name:
                  ru: .png
            - value: '.gif'
              name:
                  ru: .gif
        default: '.png'
```

### Добавление спутников
В этой вкладке пользователь добавляет уже собственные спутники, ради запуска которых он и хочет получить модель. Это реализуется через всплывающее окно. Тут он указывает широту и долготу места нахождения этих аппаратов, а также модули их скоростей (точнее, радиальные компоненты скоростей) и цвета маркера, которыми они будут обозначаться на графике. Как будет видно, у поля USER_SATELITE есть даже собственная внутненняя структура, так как внутри этого поля есть встроенные поля.
```python
    USER_SATELITE:
        title:
          ru: Запуск спутников
        type: object
        FIELDS:
            WIDTH_SAT:
                type: integer
                title:
                    ru: Широта
                hint:
                    ru: Введите широту в градусах, тип данных int
                min: -90
                max: 90
                default: 0

            LONG_SAT:
                type: integer
                title:
                    ru: Долгота
                hint:
                    ru: Введите долготу в градусах, тип данных int
                min: -180
                max: 180
                default: 0

            ABS_VELOCITY:
                title:
                    ru: Модуль скорости
                type: decimal
                hint:
                    ru: Направление скорости радиальное
                min: 0
                max: 20000
                default: 11800
            
            COLOR_SAT:
                type: string
                title:  
                    ru: Цвет маркера
                default: 'black'
                hint:
                    ru: Выберите из выпадающего списка цвет для обозначения маркера ВАШИХ аппартов на графике.
                enum:
                    - value: 'black'
                      name:
                        ru: Чёрный
                    - value: 'red'
                      name:
                        ru: Красный
                    - value: 'blue'
                      name:
                        ru: Синий
                    - value: 'green'
                      name:
                        ru: Зелёный
                    - value: 'yellow'
                      name:
                        ru: Жёлтый
                    - value: 'pink'
                      name:
                        ru: Розовый
        STRUCTURE:
            - group:
                key: user_satelite
                title:
                  ru: Добавить
                fields:
                    - field: WIDTH_SAT
                    - field: LONG_SAT
                    - field: ABS_VELOCITY
                    - field: COLOR_SAT
                      width: full
```

## Валидатор
Был разработан специальный валидатор, содержащий несколько методов проверки данных, получаемых от пользователя в формате JSON.
Валидатор предназначен для предотвращения ошибок ввода, так как некорректные значения могут привести к ошибкам непосредственно во время моделирования.
Если введённые данные не соответствуют требованиям, система генерирует исключение ValueError и запрещает их использование в расчётах.

Валидатор имеет следующую структуру:
```python
class Validator:
    def __init__(self, data):
        ...

    def date_examination(self):
        ...

    def start_time_examination(self):
        ...
        
    def name_examination(self):
        ...

    def __is_number(self, a):
        ...
```

Разберём её поподробнее. В методе '__init__' происходит считывание данных из полученного файла и сохарнение их в атрибуте self.data.
```python
    def __init__(self, data):
        with open(data) as data_file:
            self.data = json.load(data_file)
```

Метод 'date_examination' извлекает значение введённой пользователем даты и через ряд условий проверяет её правильность:
- Полученная строка не должна быть пустой. Точек, разделяющих значения не должно быть больше 3.
- Количество дней в феврале (не может быть больше 28 или 29 дней).
- Корректность месяца (от 1 до 12).
- Корректность дня (не может быть меньше 1 или больше 30(31) в зависимости от месяца)
Если дата неверна, вызывается исключение.
```python
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
```

Через 'start_time_examination' проверяется правильность введённого времени отсчёта:
- Часы должны быть от 0 до 23.
- Минуты и секунды должны быть от 0 до 59.
```python
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
```

В методе 'name_examination' происходит проверка на количество символов в названии файла (их не должно быть меньше 4).
```python
    def name_examination(self):
            name = self.data["graf_settings"]["FILE_NAME"]["value"]
            if len(name) < 4:
                print(f'Ошибка в значении "{name}"')
                raise ValueError
```

Остался последний, вспомогательный, метод - '__is_number'. Он используется в основных методах для выяснения,
являются ли строки, извлечённые из данных через '.split()', целыми числами.
```python
    def name_examination(self):
            name = self.data["graf_settings"]["FILE_NAME"]["value"]
            if len(name) < 4:
                print(f'Ошибка в значении "{name}"')
                raise ValueError
```

### Запуск валидатора и установка по умолчанию актуальной даты
Запускается весь код следующим образом:
```python
def run_validator(data_path):
    valid = validator.Validator(data_path)
    valid.date_examination()
    valid.start_time_examination()
```

В качестве даты по умолчанию в поле должно всегда стоять актуальное число. Для этого была создана функция 'change_time'.
При помощи библиотеки datetime мы получаем значение актуальной даты, а затем подставляем её по ключу в поле для даты.
```python
def change_time(path):
    with open(path, encoding="UTF-8") as f:
        data = yaml.safe_load(f)

    now = datetime.datetime.now().date()
    now = f'{now.day}.{now.month}.{now.year}'

    data['FIELDS']['DATE']['default'] = now
    with open("frontend/src/values.yaml", "w", encoding="UTF-8") as f:
        yaml.dump(data, f, allow_unicode=True)
```

Так как мы создаём графический интерфейc на сайте AstroModel, чтобы прописать поля, нам нужно использовать Yaml, потому что это обязательный формат для него.