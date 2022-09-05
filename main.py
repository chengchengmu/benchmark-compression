#!/usr/bin/env python3
import time
import gzip
import snappy
import plotly.express as px

data = open("Linux_2k.log").readlines()

data_bytes = ''.join(data).encode('utf-8')

algo = []
duration = []
rate = []



# Gzip^^
for i in range(10):
    algo.append(f"gzip-{i}")
    t = time.process_time()
    # compress
    compressed = gzip.compress(data_bytes, compresslevel=i)
    elapsed = time.process_time() - t
    duration.append(elapsed)
    rate.append(len(data_bytes)/len(compressed))


algo.append("snappy")
t = time.process_time()
# compress
compressed = snappy.compress(data_bytes)
elapsed = time.process_time() - t
duration.append(elapsed)
rate.append(len(data_bytes)/len(compressed))

fig = px.line(x=algo, y=duration, title="compression time")
print(fig)
fig.show()

fig = px.line(x=algo, y=rate, title="compression rate")
print(fig)
fig.show()

# TODO plot decompression time
