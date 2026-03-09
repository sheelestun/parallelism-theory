import matplotlib.pyplot as plt
import numpy as np

# Чтение данных из файла
data = np.loadtxt('speedup_data.txt', comments='#')
threads = data[:, 0]
speedup = data[:, 2]

print(f"Loaded data:")
print(f"Threads: {threads}")
print(f"Speedup: {speedup}")

# Создание фигуры
plt.figure(figsize=(10, 7))

# График идеального ускорения (линейное)
max_p = int(max(threads))  # 🔧 Приводим к int!
p_range = np.arange(1, max_p + 1)
plt.plot(p_range, p_range, '--', color='darkblue', linewidth=2, label='Linear', zorder=1)

# График реального ускорения
plt.plot(threads, speedup, 'o-', color='coral', linewidth=2, markersize=8, 
         label=f'M = {40000000:,}'.replace(',', ' '), zorder=2)

# Оформление графика
plt.xlabel('p', fontsize=12, fontweight='bold')
plt.ylabel(r'$S_p$', fontsize=12, fontweight='bold')
plt.title('Speedup vs Number of Threads', fontsize=14, fontweight='bold', pad=20)

# Настройка осей - тоже используем int
plt.xticks(threads)
plt.yticks(range(0, max_p + 2, 1))  # 🔧 max_p уже int
plt.grid(True, linestyle='-', alpha=0.3, linewidth=0.5)

# Легенда
plt.legend(loc='upper left', fontsize=10, framealpha=0.9)

# Добавление подписи с размером задачи
plt.text(0.65, 0.3, f'M = {40000000:,}', transform=plt.gca().transAxes, 
         fontsize=11, fontweight='bold', 
         bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.7))

# Настройка границ графика
plt.xlim(min(threads) - 0.5, max(threads) + 0.5)
plt.ylim(0, max_p + 1)

# Сохранение и показ
plt.tight_layout()
plt.savefig('speedup_graph.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nGraph saved as speedup_graph.png")