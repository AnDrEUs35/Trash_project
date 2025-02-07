import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from geopy.distance import geodesic

# Функция для генерации случайных точек
def generate_random_points(num_points=100):
    latitudes = np.random.uniform(-90, 90, num_points)
    longitudes = np.random.uniform(-180, 180, num_points)
    return list(zip(latitudes, longitudes))

# Вводим координаты человека и радиус видимости
person_location = (50.7558, 108.6173)  # Пример: Москва (широта, долгота)
radius_km = 400  # Радиус видимости в километрах

# Генерируем случайные точки
np.random.seed(42)  # Для воспроизводимости
points = generate_random_points(100)

# Фильтрация точек в радиусе
in_visibility = []  # Для точек в радиусе
for point in points:
    distance = geodesic(person_location, point).km
    if distance <= radius_km:
        in_visibility.append(point)

# Создаём карту
fig = plt.figure(figsize=(10, 10), dpi=200)  # Увеличиваем dpi для четкости
ax = plt.axes(projection=ccrs.PlateCarree())

# Устанавливаем границы карты
# Вычисляем ширину и долготу эквивалентную радиусу
lat_per_km = 1 / 111.0  # 1 градус широты в км
long_per_km = lat_per_km * np.cos(np.radians(person_location[0]))  # 1 градус долготы в км

# Расчёт buffer в градусах
buffer_lat = radius_km * lat_per_km
buffer_long = radius_km * long_per_km

ax.set_extent([
    person_location[1] - buffer_long, person_location[1] + buffer_long,
    person_location[0] - buffer_lat, person_location[0] + buffer_lat],
    crs=ccrs.PlateCarree()
)

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
ax.set_title(f'Карта вокруг человека на координатах {person_location} с радиусом {radius_km} км', fontsize=15)
plt.legend(loc='upper right')
plt.savefig('hopeful')
