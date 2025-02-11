#imports
import numpy as np
import json
import math
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from geopy.distance import geodesic

def project_orbit_to_earth(x, y, z, R=6371):
    """
    Проецирует точку с орбиты на поверхность Земли и возвращает географические координаты"""
    # 1. Координаты проекции на поверхности Земли
    z, y = y, z # теперь все четко должно быть
    magnitude = math.sqrt(x**2 + y**2 + z**2)
    x_proj = (x / magnitude) * R
    y_proj = (y / magnitude) * R
    z_proj = (z / magnitude) * R

    # 2. Преобразование в географические координаты
    latitude = math.asin(z_proj / R)
    longitude = math.atan2(y_proj, x_proj)

    # Перевод в градусы
    latitude_degrees = math.degrees(latitude)
    longitude_degrees = math.degrees(longitude)

    return latitude_degrees, longitude_degrees


class Map:
    def __init__(self, data):
        self.FloatType = np.float64
        self.IntType = np.int32
        self.pos_sattelite = []
        self.pos_trash = []
        with open(data, 'r') as file:
            self.data = json.load(file)

    def get_info(self):
        #satellites parametrs
        n_sat = len(self.data['satellites'])
        sat_names = np.array([self.data['satellites'][i]['name'] for i in range(n_sat)])
        self.pos_sattelite = np.zeros([n_sat, 3], dtype=self.FloatType)
        
        #trash parametrs
        n_tr = len(self.data['trash'])
        self.pos_trash = np.zeros([n_tr, 3], dtype=self.FloatType) 

        #filling pos of satellites and trash
        for i in range(n_sat):
            for j in range(3):
                self.pos_sattelite[i][j] = self.FloatType(self.data['satellites'][i]['coords'][j])
        
        for i in range(n_tr):
            for j in range(3):
                self.pos_trash[i][j] = self.FloatType(self.data['trash'][i]['coords'][j])

        # НАЧАЛО ДЛЯ 2D
    def get_map(self, person_location, radius_km):
        if radius_km < 1:
            radius_km = 1 # Защита от бед
            
        pos_sattelite = list(self.pos_sattelite) + list(self.pos_trash) #спутники и мусор
        points = [project_orbit_to_earth(x, y, z,) for x, y, z in pos_sattelite] 

                # Фильтрация точек в радиусе
        in_visibility = []  # Для точек в радиусе
        for point in points:
            distance = geodesic(person_location, point).km
            if distance <= radius_km:
                in_visibility.append(point)

        # Вычисляем ширину и долготу эквивалентную радиусу
        lat_per_km = 1 / 111.0  # 1 градус широты в км
        long_per_km = lat_per_km * np.cos(np.radians(person_location[0]))  # 1 градус долготы в км

        # Расчёт buffer в градусах
        buffer_lat = radius_km * lat_per_km
        buffer_long = radius_km * long_per_km

        # Если радиус слишком большой, установить границы карты на максимальные значения
        max_lat = 90
        min_lat = -90
        max_lon = 180
        min_lon = -180


        if radius_km > 20000:  # Настройка предела, например, 20000 км
            extent = [min_lon, max_lon, min_lat, max_lat]
        else:
            extent = [
                person_location[1] - buffer_long,
                person_location[1] + buffer_long,
                person_location[0] - buffer_lat,
                person_location[0] + buffer_lat
            ]
        # Создаём карту
        fig = plt.figure(figsize=(8, 8), dpi=200)  # Увеличиваем dpi для четкости и делаем квадратную
        ax = plt.axes(projection=ccrs.PlateCarree())

        # Устанавливаем границы карты
        ax.set_extent(extent, crs=ccrs.PlateCarree())

        # Добавляем основной фон карты
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.LAKES, edgecolor='black')
        ax.add_feature(cfeature.RIVERS)

        # Отображаем точки в пределах видимости
        if in_visibility:
            in_visibility_lats, in_visibility_longs = zip(*in_visibility)
            ax.scatter(in_visibility_longs, in_visibility_lats, color='blue', label='В радиусе видимости', alpha=0.7, transform=ccrs.PlateCarree())

        # Отображаем местоположение человека
        ax.scatter(person_location[1], person_location[0], color='red', marker='x', s=150, label='Человек', transform=ccrs.PlateCarree())

        # Добавляем сетку (широта и долгота)
        gridlines = ax.gridlines(draw_labels=True, linestyle='--', color='gray', alpha=0.5)
        gridlines.xlabels_top = False
        gridlines.ylabels_right = False


        # Заголовок и легенда
        ax.set_title(f'Карта вокруг человека на координатах {person_location} с радиусом {radius_km} км', fontsize=13)
        plt.legend(loc='upper right')

        # Устанавливаем аспект (чтобы карта была квадратной)
        ax.set_aspect('equal', adjustable='datalim')

        #plt.axis('equal')  # Делаем оси равными, чтобы картинка была квадратной
        plt.savefig('result')

