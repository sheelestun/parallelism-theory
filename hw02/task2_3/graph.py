import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('speedup_data.txt', comments='#')

threads = data[0:11, 0]
speedup_v1 = data[0:11, 2]        
speedup_v2 = data[11:22, 2]       

plt.figure(figsize=(10, 6))
plt.plot(threads, threads, '--', color='gray', label='Linear', alpha=0.5)

# Version 1 и Version 2
plt.plot(threads, speedup_v1, 'o-', linewidth=2, label='Version 1')
plt.plot(threads, speedup_v2, 's-', linewidth=2, label='Version 2')

plt.xlabel('p', fontsize=12)
plt.ylabel('S', fontsize=12)
plt.title('Speedup: Simple Iteration Method', fontsize=14)
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)
plt.xticks(threads)

plt.savefig('speedup_graph.png', dpi=300, bbox_inches='tight')
print("Graph saved to speedup_graph.png")
