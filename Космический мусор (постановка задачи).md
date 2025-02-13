## 1. Направление: Анализ данных

###### Алгоритм получения данных
```python
import sys

from sgp4.api import Satrec
from astropy.time import Time
from astropy.coordinates import TEME

import h5py

############## Data analis ##############
s = '1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991'
t = '2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482'

satellite = Satrec.twoline2rv(s, t)

t = Time(2458827.362605, format='jd')
error_code, teme_p, teme_v = satellite.sgp4(t.jd1, t.jd2)  # in km and km/s

print(teme_p, 'km')
print(teme_v, 'km/s')

```

###### Результат
```bash
(-6102.443276428913, -986.3320160861297, -2820.3130707199225) km
(-1.4552527284474308, -5.527413835655969, 5.101042029427083) km/s
```

###### Задача
[[_Наблюдательная астрометрия_]]
Разобраться хотя бы в минимальном представлении как строятся небесные координаты и как они преобразуются. Научиться работать с системами координат при помощи библиотеки [astropy](https://docs.astropy.org/en/stable/index.html). Разобраться с TLE форматом данных, представляющих собой набор элементов орбиты для спутника Земли (на его основе реализована библиотека [sgp4](https://pypi.org/project/sgp4/)) и специальной координатной системе TEME (True Equator Mean Equinox frame). 

## 2. Направление: Моделирование и обработка результатов моделирования

###### Алгоритм создания файла с начальными условиями для моделирования
```python
############## AREPO implemetation ##############
FloatType = np.float64
IntType = np.int32

mass_earth = np.array([5.6e24])
num_part_2 = 1000
mass_sat = np.ones(num_part_2, dtype=FloatType)

pos_earth = np.zeros([1, 3], dtype=FloatType)
vel_earth = np.zeros([1, 3], dtype=FloatType)

IC = h5py.File('/IC.hdf5', 'w')

header = IC.create_group("Header")
part1 = IC.create_group("PartType1") # Earth
part2 = IC.create_group("PartType2") # Debris
 
NumPart = np.array([0, 1, num_part_2, 0, 0, 0], dtype = IntType)
header.attrs.create("NumPart_ThisFile", NumPart)
header.attrs.create("NumPart_Total", NumPart)
header.attrs.create("NumPart_Total_HighWord", np.zeros(6, dtype = IntType))
header.attrs.create("MassTable", np.zeros(6, dtype = IntType))
header.attrs.create("Time", 0.0)
header.attrs.create("Redshift", 0.0)
header.attrs.create("BoxSize", BoxSize)
header.attrs.create("NumFilesPerSnapshot", 1)
header.attrs.create("Omega0", 0.0)
header.attrs.create("OmegaB", 0.0)
header.attrs.create("OmegaLambda", 0.0)
header.attrs.create("HubbleParam", 1.0)
header.attrs.create("Flag_Sfr", 0)
header.attrs.create("Flag_Cooling", 0)
header.attrs.create("Flag_StellarAge", 0)
header.attrs.create("Flag_Metals", 0)
header.attrs.create("Flag_Feedback", 0)
header.attrs.create("Flag_DoublePrecision", 1)

part1.create_dataset("ParticleIDs", data=np.arange(0, 1))
part1.create_dataset("Coordinates", data=pos_earth)
part1.create_dataset("Masses", data=mass_earth)
part1.create_dataset("Velocities", data=vel_earth)

part2.create_dataset("ParticleIDs", data=np.arange(1, num_part_1 + num_part_2 + 1))
part2.create_dataset("Coordinates", data=teme_p)
part2.create_dataset("Masses", data=mass_sat)
part2.create_dataset("Velocities", data=teme_v)

## close file
IC.close()
sys.exit(0)
```

###### Задача
Разобраться в имплементации данных в библиотеку численного моделирования AREPO code. Оформить полученные данные в формате hdf5, соответствующему api библиотека численного моделирования AREPO. Разобраться с ParaWieve. Написать скрипт, который по заданной дате и широте показывает наличие в некоторой области вокруг этой широты положение мусора и свободные участки. В качестве иллюстрации можно использовать вот этот [проект](https://geoxc-apps.bd.esri.com/space/satellite-explorer/).

## 3. Направление: Имплементация в Astromodel research

###### Алгоритм парсинга данных
```python
import solver
import parser
import sys 


def main(data_path: str=None, output_path: str=None) -> None:

    if data_path == None and output_path == None:
        _, data_path, output_path, *_ = sys.argv

    model_data = parser.Parser(data_path)
    model_solver = solver.Solver(model_data)
    model_solver.run_solve(output_path)


if __name__ == "__main__":
    main('./output.json', '.')
```

```python
import json

class Parser:
    def __init__(self, data):
        with open(data) as data_file:
            self.data = json.load(data_file)
    

    def get_coords(self):
        coords = self.data['plot_data']
        return (coords['x_coords']['value'], 
                coords['y_coords']['value'])


    def get_plot_args(self):
        return self.data['plot_data']


    def get_fig_parms(self):
        return self.data['plot_data']
```

```python
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
```

```json
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
```

```yaml
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

```

###### Задача
Разобраться с api платформы Astromodel Research. Создать конфигуратор и парсер для направлений 1 и 2.