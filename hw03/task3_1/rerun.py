import subprocess
import numpy as np
import re

NUM_RUNS = 50
EXECUTABLE = './test.out'
OUTPUT_FILE = 'speedup_data_averaged.txt'
THREADS = [1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40]

results = {}
pattern = re.compile(r'p=\s*(\d+):\s*([\d.]+)s')
size_pattern = re.compile(r'#\s*Matrix size:\s*(\d+)')

for run in range(NUM_RUNS):
    try:
        result = subprocess.run([EXECUTABLE], capture_output=True, text=True, timeout=600)
    except:
        continue
    
    size = None
    for line in result.stdout.split('\n'):
        m = size_pattern.search(line)
        if m:
            size = int(m.group(1))
            if size not in results:
                results[size] = {t: [] for t in THREADS}
            continue
        if not line.strip() or line.startswith('#'):
            continue
        match = pattern.search(line)
        if match and size:
            t = int(match.group(1))
            time_val = float(match.group(2))
            if t in THREADS and time_val > 0:
                results[size][t].append(time_val)

with open(OUTPUT_FILE, 'w') as f:
    for size in sorted(results):
        r = results[size]
        f.write(f"# Matrix size: {size}x{size}\n")
        f.write(f"# Runs: {NUM_RUNS}\n")
        f.write("# Threads MeanTime StdDev Speedup Efficiency\n")
        
        t1 = np.mean(r[1]) if r[1] else 1.0
        for t in THREADS:
            if not r[t]:
                continue
            mean_t = np.mean(r[t])
            std_t = np.std(r[t])
            speedup = t1 / mean_t if mean_t > 0 else 0
            eff = speedup / t * 100 if t > 0 else 0
            f.write(f"{t:3d} {mean_t:.6f} {std_t:.6f} {speedup:.4f} {eff:.2f}%\n")
        f.write("\n")