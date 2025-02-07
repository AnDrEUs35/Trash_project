import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Списки спутников и мусора (начала и конца)
satellites_start = [(55.7558, 37.6173), (34.0522, -118.2437)]  # Начальные координаты спутников
satellites_end = [(48.8566, 2.3522), (51.5074, -0.1278)]        # Конечные координаты спутников
debris_start = [(42.3601, -71.0589), (40.7128, -74.0060)]      # Начальные координаты мусора
debris_end = [(55.9533, -3.1883), (35.6895, 139.6917)]         # Конечные координаты мусора

# Установка границ карты
extent = [-180, 180, -90, 90]

# Создаем карту
fig = plt.figure(figsize=(10, 10), dpi=200)  
ax = plt.axes(projection=ccrs.PlateCarree())

# Устанавливаем границы карты
ax.set_extent(extent, crs=ccrs.PlateCarree())

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

# Добавляем сетку (широта и долгота)
gridlines = ax.gridlines(draw_labels=True, linestyle='--', color='gray', alpha=0.5)
gridlines.xlabels_top = False
gridlines.ylabels_right = False

# Заголовок и легенда
ax.set_title('Карта спутников и мусора с перемещениями', fontsize=15)

# Показать карту
plt.savefig('more_lists')
