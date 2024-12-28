import matplotlib.pyplot as plt


class Solver:
    def __init__(self, model_data):
        self.coords = model_data.get_coords()
        self.plot_args = model_data.get_plot_args()
        self.fig_parameters = model_data.get_fig_parms()
    

    def run_solve(self, output_path):
        plt.plot(*self.coords, 
                 marker=self.plot_args['marker']['value'],
                 color=self.plot_args['color']['value'],
                 ms=self.plot_args['ms']['value'],
                 label=self.plot_args['label']['value'])

        if 'grid' in self.fig_parameters:
            plt.grid()
        if 'label' in self.plot_args:
            plt.legend()
        if 'title' in self.fig_parameters:
            plt.title(self.fig_parameters['title']['value'])
        
        plt.savefig(f'{output_path}/result.png')
{
    "plot_data":{
        "x_coords":{
            "value": [3, 8, 5]
        },
        "y_coords": {
            "value": [7, 4, 9]
        },
        "color":{
            "value": "g"
        },
        "label":{
            "value": "Graf 1"
        },
        "marker":{
            "value": ">"
        }, 
        "ms":{
            "value": 5
        }, 
        "title":{
            "value": "Test pythons libs"
        }
    }
}

'''
FIELDS:
    ################ For Config.sh #######################
    NTYPES:
        type: integer
        title:
            ru: Количество типов частиц
        hint:
            ru:
                Определение количества типов частиц. Как правило  по умоланию их шесть и
                крайне редко необходимо больше.
        min: 6
        default: 6
        max: 20
    LONG_X:
        type: integer
        title:
            ru: Растяжение пространтсва вдоль оси X
        hint:
            ru:
                Изменение размера пространства моделирования вдоль  оси X, обязателен тип
                данных int
        default: 1
    LONG_Y:
        type: integer
        title:
            ru: Растяжение пространтсва вдоль оси Y
        hint:
            ru:
                Изменение размера пространства моделирования вдоль  оси Y, обязателен тип
                данных int
        default: 1
    DIMS:
        type: string
        view: radio
        title:
            ru: Размерность пространства
        enum:
            - value: TWODIMS
              name:
                  ru: Двумерное
            - value: THREEDIMS
              name:
                  ru: Трехмерное
        default: THREEDIMS
    REGULARIZE_MESH_FACE_ANGLE:
        type: boolean
        title:
            ru: Параметры сетки
        hint:
            ru: Определение механизма уточнения динамической сетки
        default: true
    INPUT_IN_DOUBLEPRECISION:
        type: boolean
        title:
            ru: Точность входных параметров (double)
        hint:
            ru:
                Определение входной точности чисел, лучше  всегда оставить по умолчанию
                этот ключ
        default: true
    SnapshotFileBase:
        type: string
        title:
            ru: Название выходных файлов
        default: snap
    TimeLimitCPU:
        type: integer
        units: time
        title:
            ru: Максимальная длительность расчёта
        default: 9000
    UnitVelocity_in_cm_per_s:
        type: decimal
        units: velocity
        title:
            ru: Единицы измерения скорости в "см/с"
        default: 1
    UnitLength_in_cm:
        type: decimal
        units: lenght
        title:
            ru: Единицы измерения длины в "см"
        default: 1
    UnitMass_in_g:
        type: decimal
        units: mass
        title:
            ru: Единицы измерения массы в "г"
        default: 1
    PeriodicBoundariesOn:
        type: integer
        title:
            ru: Переодические граничные условия
        enum:
            - value: 1
              name:
                  ru: переодические
            - value: 0
              name:
                  ru: непереодические
        default: 1

STRUCTURE:
    - group:
          key: config
          title:
              ru: Основные поля
          fields:
              - separator:
                    title:
                        ru: Ключи с численными значениями
              - field: NTYPES
    - group:
          key: parameters
          title:
              ru: Настройка объектов
          fields:
              - separator:
                    title:
                        ru: Настройки ввода / вывода информации
              - field: InitCondFile
                view: dropdown
              - field: SnapshotFileBase
                width: half
    - group:
          key: IC_data
          title:
              ru: Создание объектов и частиц
          fields:
              - field: massive_particle
              - field: gas_particles
UNITS:
    lenght:
        cm:
            title:
                ru: Сантиметры
            m: 1000
        m:
            title:
                ru: Метры
            cm: 0.001
    mass:
        kg:
            title:
                ru: Килограммы
            g: 1000
        g:
            title:
                ru: Граммы
            kg: 0.001
    time:
        min:
            title:
                ru: Минуты
            s: 0.01666666666
        s:
            title:
                ru: Секунды
            min: 60
    velocity:
        m/s:
            title:
                ru: Метры в секунду
            km/h: 3.6
        km/h:
            title:
                ru: Километры в час
            m/s: 0.27777777777
'''