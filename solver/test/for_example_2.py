import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Функция, чтобы генерировать данные, например, случайные точки
def generate_random_points(num_points=100):
    # Генерируем случайные широты и долготы
    latitudes = np.random.uniform(-90, 90, num_points)
    longitudes = np.random.uniform(-180, 180, num_points)
    return list(zip(latitudes, longitudes))

# Координаты человека (широта, долгота)
person_location = (55.7558, 37.6173)  # Пример: Москва
radius_km = 10000  # Радиус в километрах

# Генерируем случайные точки
points = generate_random_points(1000)

# Подготовка для визуализации
in_zone = []
out_zone = []

# Определяем точки, которые находятся в радиусе
for point in points:
    distance = geodesic(person_location, point).km
    if distance <= radius_km:
        in_zone.append(point)
    else:
        out_zone.append(point)

# Параметры отображаемой области карты
delta_lat = radius_km // 111 
delta_lon = radius_km // 111 

# Отрисовка карты
plt.figure(figsize=(8, 6))

# Отображаем точки в зоне
if in_zone:
    in_zone_lats, in_zone_longs = zip(*in_zone)
    plt.scatter(in_zone_longs, in_zone_lats, color='blue', label='В зоне', alpha=0.5)

# Отображаем точки вне зоны
if out_zone:
    out_zone_lats, out_zone_longs = zip(*out_zone)
    plt.scatter(out_zone_longs, out_zone_lats, color='red', label='Вне зоны', alpha=0.5)

# Отметка местоположения человека
plt.scatter(person_location[1], person_location[0], color='green', marker='x', s=100, label='Человек')

# Настройка границ области
plt.xlim(person_location[1] - delta_lon, person_location[1] + delta_lon)
plt.ylim(person_location[0] - delta_lat, person_location[0] + delta_lat)

plt.title(f'Точки в радиусе {radius_km} км от человека')
plt.xlabel('Долгота')
plt.ylabel('Широта')
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.axvline(0, color='black', lw=0.5, ls='--')
plt.grid()
plt.legend()
plt.savefig('photo2')