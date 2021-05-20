import numpy as np
import matplotlib.pyplot as plt


def plot(population_fitness_stats):
    data = np.array(population_fitness_stats)
    average = data[:, 0]
    print(average)
    minimum = data[:, 1]
    print(minimum)
    maximum = data[:, 2]
    print(maximum)
    generation = np.arange(1, len(data) + 1, 1)
    print(generation)

    plt.plot(generation, maximum, color='red', label='maximum')
    plt.plot(generation, average, color='green', label='average')
    plt.plot(generation, minimum, color='blue', label='minimum')
    plt.xlabel('Generation')
    plt.ylabel('Fitness Value')
    plt.legend(loc='upper left')
    plt.grid()
    plt.show()
