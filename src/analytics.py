# analytics.py

import matplotlib.pyplot as plt

def show_analytics():
    sizes = [2**i for i in range(1, 8)]
    conventional_times = [size**3 for size in sizes]
    strassen_times = [size**2.81 for size in sizes]

    plt.figure()
    plt.plot(sizes, conventional_times, label="Conventional O(n^3)")
    plt.plot(sizes, strassen_times, label="Strassen O(n^2.81)")
    plt.xlabel("Matrix Size (n)")
    plt.ylabel("Time Complexity")
    plt.legend()
    plt.title("Time Complexity Comparison")
    plt.grid(True)
    plt.show()