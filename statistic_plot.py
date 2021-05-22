import numpy as np
import matplotlib.pyplot as plt


def plot(population_fitness_stats, minimum_maximum_plot=False):
    data = np.array(population_fitness_stats)
    average = data[:, 0]
    minimum, maximum = None, None
    if minimum_maximum_plot:
        minimum = data[:, 1]
        maximum = data[:, 2]
    generation = np.arange(1, len(data) + 1, 1)
    if minimum_maximum_plot:
        plt.plot(generation, maximum, color='red', label='maximum')
    plt.plot(generation, average, color='green', label='average')
    if minimum_maximum_plot:
        plt.plot(generation, minimum, color='blue', label='minimum')
    plt.xlabel('Generation')
    plt.ylabel('Fitness Value')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()
