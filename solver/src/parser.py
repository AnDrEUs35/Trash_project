#imports
import numpy as np
import h5py
import json
import math
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from geopy.distance import geodesic

def to_sphere_system(x,y,z):
    # z -> y
    # x -> x
    # y -> z 
    z, y = y, z # теперь все четко должно быть
    r = ( x**2 + y**2 + z**2 )**0.5 # радиус вектор 
    polar = np.atan( (( x**2 + y**2)**0.5) / z ) * 180 / np.pi # зенит в градусах 
    phi = np.atan2(y, x) * 180 / np.pi #азимут в граудусах 
    return r, polar, phi

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



class Parser:
    
    def __init__(self, data):
        self.BoxSize = 500
        self.FloatType = np.float64
        self.IntType = np.int32
        with open(data, 'r') as file:
            self.data = json.load(file)
    
    def get_hdf5(self, output_path):
        #return './../test/IC.hdf5'
        #Earth parametrs
        mass_earth = np.array([5.6e24])
        pos_earth = np.zeros([1, 3], dtype=self.FloatType)
        vel_earth = np.zeros([1, 3], dtype=self.FloatType)

        global pos_sattelite, pos_trash
        #satellites parametrs
        n_sat = len(self.data['satellites'])
        sat_names = np.array([self.data['satellites'][i]['name'] for i in range(n_sat)])
        pos_sattelite = np.zeros([n_sat, 3], dtype=self.FloatType)
        vel_sattelite = np.zeros([n_sat, 3], dtype=self.FloatType)
        mass_sat = np.ones(n_sat, dtype=self.FloatType)
        
        
        #trash parametrs
        n_tr = len(self.data['trash'])
        tr_indexes = np.array([self.data['trash'][i]['index'] for i in range(n_tr)])
        pos_trash = np.zeros([n_tr, 3], dtype=self.FloatType)
        vel_trash = np.zeros([n_tr, 3], dtype=self.FloatType)
        mass_trash = np.ones(n_tr, dtype=self.FloatType)
        
        
        #filling pos and vel of satellites and trash
        for i in range(n_sat):
            for j in range(3):
                pos_sattelite[i][j] = self.FloatType(self.data['satellites'][i]['coords'][j])
                vel_sattelite[i][j] = self.FloatType(self.data['satellites'][i]['velocity'][j])
        
        for i in range(n_tr):
            for j in range(3):
                pos_trash[i][j] = self.FloatType(self.data['trash'][i]['coords'][j])
                vel_trash[i][j] = self.FloatType(self.data['trash'][i]['velocity'][j])
        
        
        #open file
        IC = h5py.File('/workspaces/Trash_project/solver/test/IC.hdf5', 'w')
        
        #creating groups
        header = IC.create_group("Header")
        part1 = IC.create_group("satellites") #
        part2 = IC.create_group("trash") #
        part3 = IC.create_group("Earth") #
        
        #header
        NumPart = np.array([0, 1, n_tr, 0, 0, 0], dtype = self.IntType)
        header.attrs.create("NumPart_ThisFile", NumPart)
        header.attrs.create("NumPart_Total", NumPart)
        header.attrs.create("NumPart_Total_HighWord", np.zeros(6, dtype = self.IntType))
        header.attrs.create("MassTable", np.zeros(6, dtype = self.IntType))
        header.attrs.create("Time", 0.0)
        header.attrs.create("Redshift", 0.0)
        header.attrs.create("BoxSize", self.BoxSize)
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
        
        #satellites
        part1.create_dataset("ParticleIDs", data=np.arange(1, n_sat + 1))
        part1.create_dataset("Coordinates", data=pos_sattelite)
        part1.create_dataset("Masses", data=mass_sat)
        part1.create_dataset("Velocities", data=vel_sattelite)
        
        #trash
        part2.create_dataset("ParticleIDs", data=np.arange(n_sat + 1, n_sat + n_tr + 1))
        part2.create_dataset("Coordinates", data=pos_trash)
        part2.create_dataset("Masses", data=mass_trash)
        part2.create_dataset("Velocities", data=vel_trash)
        
        #Earth
        part3.create_dataset("ParticleIDs", data=np.arange(0, 1))
        part3.create_dataset("Coordinates", data=pos_earth)
        part3.create_dataset("Masses", data=mass_earth)
        part3.create_dataset("Velocities", data=vel_earth)
        
        # close file
        IC.close()
    



        # НАЧАЛО ДЛЯ 2D
    def get_map(self, person_location, radius_km):
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

    

    def get_user_graphical_data(self):
        # От сюда нам надо получить область нужную пользователю (радиус поражения)
        pass
