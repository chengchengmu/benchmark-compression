#!/usr/bin/env python3
import time
import click
import plotly.graph_objects as go

import gzip
import snappy
import zstd

def zstd_compress(level):
    def f(data):
        return zstd.compress(data, level)
    return f

@click.command()
@click.option('-d', '--data-file', default="data/Linux_2k.log")
def main(data_file):
    data = open(data_file).readlines()

    data_bytes = ''.join(data).encode('utf-8')

    algo = []
    duration = []
    rate = [] # compression rate

    def measure_compress(label, compress, data, **kwargs):
        s = len(data)
        algo.append(label)
        t = time.process_time()
        compressed = compress(data, **kwargs)
        elapsed = time.process_time() - t
        duration.append(elapsed)
        rate.append(s/len(compressed))

    # Gzip
    for i in range(1, 10):
        measure_compress(f"gzip, level={i}", gzip.compress, data_bytes, compresslevel=i)


    # Snappy
    measure_compress("snappy", snappy.compress, data_bytes)

    # Zstd
    for level in range(-100, -1, 10):
        measure_compress(f"zstd, level={level}", zstd_compress(level), data_bytes)
    # Zstd can go up to 22 but beyond 15, we don't observe much gain
    for level in range(-1, 16):
        measure_compress(f"zstd, level={level}", zstd_compress(level), data_bytes)

    fig = go.Figure(data=go.Scatter(x=rate,
                                    y=duration,
                                    mode='markers',
                                    text=algo)
                    )

    fig.update_layout(title=f"Compression rate and time on {data_file}")
    fig.show()

if __name__ == "__main__":
    main()
