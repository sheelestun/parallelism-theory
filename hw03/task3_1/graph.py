import matplotlib.pyplot as plt
import numpy as np
import re

def read_data(filename):
    data, size = {}, None
    with open(filename) as f:
        for line in f:
            line = line.strip()
            m = re.match(r'#\s*Matrix size:\s*(\d+)', line)
            if m:
                size = int(m.group(1))
                data[size] = {'t': [], 's': []}
                continue
            if line.startswith('#') or not line:
                continue
            p = line.split()
            if len(p) >= 4 and size:
                try:
                    data[size]['t'].append(int(p[0]))
                    data[size]['s'].append(float(p[3]))
                except: pass
    return data

def plot(data):
    plt.figure(figsize=(10, 7))
    colors = ['coral', 'steelblue']
    max_p = max((max(d['t']) for d in data.values()), default=40)
    
    for i, size in enumerate(sorted(data)):
        d = data[size]
        if d['t']:
            plt.plot(d['t'], d['s'], 'o-', color=colors[i%2], 
                    linewidth=2, markersize=6, label=f'N={size}')
    
    plt.plot(range(1, max_p+1), range(1, max_p+1), '--', 
             color='darkblue', linewidth=1.5, label='Linear')
    
    plt.xlabel('p', fontweight='bold')
    plt.ylabel(r'$S_p$', fontweight='bold')
    plt.title('Speedup', fontweight='bold', pad=20)
    plt.xticks(sorted(set(t for d in data.values() for t in d['t'])))
    plt.yticks(range(0, max_p+2, 2))
    plt.grid(alpha=0.3)
    plt.legend(loc='upper left')
    plt.xlim(0.5, max_p+0.5)
    plt.ylim(0, max_p+1)
    plt.tight_layout()
    plt.savefig('speedup_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    plot(read_data('speedup_data_averaged.txt'))