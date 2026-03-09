import matplotlib.pyplot as plt
import numpy as np

# Чтение данных из файла
sizes = [20000, 40000]
colors = ['coral', 'steelblue']
labels = [f'M = {s:,}'.replace(',', ' ') for s in sizes]

plt.figure(figsize=(10, 7))

# Построение кривых для каждого размера
for idx, size in enumerate(sizes):
    # Читаем блок данных для текущего размера
    with open('speedup_data.txt', 'r') as f:
        lines = f.readlines()
    
    threads, speedups = [], []
    found = False
    for line in lines:
        if f'# Size = {size}' in line:
            found = True
            continue
        if found and line.startswith('# Threads'):
            continue
        if found and line.strip() == '':
            break
        if found and not line.startswith('#'):
            parts = line.split()
            if len(parts) == 3:
                threads.append(float(parts[0]))
                speedups.append(float(parts[2]))
    
    threads = np.array(threads)
    speedups = np.array(speedups)
    
    # График реального ускорения
    plt.plot(threads, speedups, 'o-', color=colors[idx], linewidth=2, 
             markersize=6, label=labels[idx], zorder=2)

# График идеального ускорения
max_p = 40
p_range = np.arange(1, max_p + 1)
plt.plot(p_range, p_range, '--', color='darkblue', linewidth=1.5, label='Linear', zorder=1)

# Оформление
plt.xlabel('p', fontsize=12, fontweight='bold')
plt.ylabel(r'$S_p$', fontsize=12, fontweight='bold')
plt.title('Speedup: Matrix-Vector Product', fontsize=14, fontweight='bold', pad=20)

plt.xticks([1, 2, 4, 6, 8, 16, 20, 40])
plt.yticks(range(0, max_p + 2, 2))
plt.grid(True, linestyle='-', alpha=0.3, linewidth=0.5)

plt.legend(loc='upper left', fontsize=10, framealpha=0.9)
plt.xlim(0.5, max_p + 0.5)
plt.ylim(0, max_p + 1)

plt.tight_layout()
plt.savefig('speedup_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graph saved as speedup_matrix.png")