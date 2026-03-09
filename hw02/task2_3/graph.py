import matplotlib.pyplot as plt
import numpy as np

# Чтение данных
data = np.loadtxt('speedup_data.txt', comments='#')
threads = data[:, 0]
time_v1 = data[0:11, 1]  # Первые 11 строк - Version 1
time_v2 = data[11:22, 1]  # Следующие 11 строк - Version 2
speedup_v1 = data[0:11, 2]
speedup_v2 = data[11:22, 2]

# График времени
plt.figure(figsize=(10, 6))
plt.plot(threads, time_v1, 'o-', linewidth=2, label='Version 1')
plt.plot(threads, time_v2, 's-', linewidth=2, label='Version 2')
plt.xlabel('Number of Threads (p)', fontsize=12)
plt.ylabel('Time (seconds)', fontsize=12)
plt.title('Execution Time vs Threads', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('time_graph.png', dpi=300)
plt.close()

# График ускорения
plt.figure(figsize=(10, 6))
max_p = max(threads)
plt.plot(range(1, max_p+1), range(1, max_p+1), '--', color='gray', label='Ideal', alpha=0.5)
plt.plot(threads, speedup_v1, 'o-', linewidth=2, label='Version 1')
plt.plot(threads, speedup_v2, 's-', linewidth=2, label='Version 2')
plt.xlabel('Number of Threads (p)', fontsize=12)
plt.ylabel('Speedup', fontsize=12)
plt.title('Speedup vs Threads', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('speedup_graph.png', dpi=300)
plt.close()

print("Graphs saved: time_graph.png, speedup_graph.png")