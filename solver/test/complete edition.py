import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# Функция для генерации случайных точек
def generate_random_points(num_points=100):
    latitudes = np.random.uniform(-90, 90, num_points)
    longitudes = np.random.uniform(-180, 180, num_points)
    return list(zip(latitudes, longitudes))

# Вводим координаты человека и радиус видимости
person_location = (50.7558, 108.6173)  # Пример: Москва (широта, долгота)
radius_km = 10000  # Радиус видимости в километрах

# Генерируем случайные точки
np.random.seed(32)  # Для воспроизводимости
satellites_start = generate_random_points(10)
satellites_end = generate_random_points(10)
debris_start = generate_random_points(10)
debris_end = generate_random_points(10)


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


# Функция для отрисовки линий
def plot_lines(start_coords, end_coords, color, label):
    for start, end in zip(start_coords, end_coords):
        start_lat, start_lon = start
        end_lat, end_lon = end
        ax.plot([start_lon, end_lon], [start_lat, end_lat], color=color, linewidth=2)
        ax.scatter(start_lon, start_lat, color=color, marker='o', s=100, transform=ccrs.PlateCarree())
        ax.scatter(end_lon, end_lat, color=color, marker='s', s=100, transform=ccrs.PlateCarree())

# Отображаем линии для спутников
plot_lines(satellites_start, satellites_end, 'blue', 'Спутники')

# Отображаем линии для мусора
plot_lines(debris_start, debris_end, 'red', 'Мусор')

# Отображаем местоположение человека
ax.scatter(person_location[1], person_location[0], color='black', marker='x', s=150, label='Человек', transform=ccrs.PlateCarree())

# Добавляем сетку (широта и долгота)
gridlines = ax.gridlines(draw_labels=True, linestyle='--', color='gray', alpha=0.5)
gridlines.xlabels_top = False
gridlines.ylabels_right = False

# Устанавливаем аспект (чтобы карта была квадратной)
ax.set_aspect('equal', adjustable='datalim')
# Заголовок и легенда
ax.set_title(f'Карта вокруг человека на координатах {person_location} с радиусом {radius_km} км', fontsize=15)
plt.legend(loc='upper right')
plt.savefig('hopeful')
