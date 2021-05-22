import random
import numpy as np
import statistic_plot as plt
from time import process_time_ns

CHROMOSOME_NUMBER = 200
LEVEL = None
FITNESS_MEMORY = dict()


def genetic_algorithm():
    population = population_generator()
    population_stats_per_generation = list()
    population_stats_per_generation.append(population_fitness_stats(population))
    start_time = process_time_ns()
    while not is_convergent(population, (lambda t: (3.33333 * (10 ** -11)) * t)(process_time_ns() -
                                                                                start_time)):
        new_population = list()
        for _ in range(len(population) - 10):
            sample_x = random_selection(population)
            sample_y = random_selection(population)
            child = crossover(sample_x, sample_y)
            if random.choices([True, False], (0.05, 0.95), k=1)[0]:
                child = mutate(child)
            new_population.append(child)
        population.sort(reverse=True, key=fitness_function)
        population = population[0:10] + new_population
        population_stats_per_generation.append(population_fitness_stats(population))
    return population, population_stats_per_generation


def max_fitness_population(population):
    max_sample = None
    max_fitness = -1 * np.inf
    for sample in population:
        if fitness_function(sample) > max_fitness:
            max_sample = sample
            max_fitness = fitness_function(sample)
    return max_sample


def population_fitness_stats(population):
    weights = [fitness_function(_) for _ in population]
    return [np.mean(weights), min(weights), max(weights)]


def is_convergent(population, limit):
    print(limit)
    weights = [fitness_function(_) for _ in population]
    print(weights)
    print(np.sqrt(np.var(np.array(weights))))
    if np.sqrt(np.var(np.array(weights))) > limit:
        return False
    else:
        return True


def population_generator():
    global CHROMOSOME_NUMBER
    initial_population = list()
    for _ in range(CHROMOSOME_NUMBER):
        sample_list = random.choices(['0', '1', '2'], (0.7, 0.15, 0.15), k=len(LEVEL))
        sample = ''
        sample = sample.join(sample_list)
        initial_population.append(sample)

    return initial_population


def random_selection(population):
    weights = list()
    fitness_values = list()
    total_sum = 0

    for sample in population:
        value = fitness_function(sample)
        fitness_values.append(value)
        total_sum += value

    for value in fitness_values:
        weights.append(value / total_sum)

    return random.choices(population=population, weights=weights, k=1)[0]


def fitness_function(sample):
    global FITNESS_MEMORY
    if sample in FITNESS_MEMORY:
        return FITNESS_MEMORY[sample]

    cost = 0
    bad_indexes = list()

    for i in range(len(LEVEL)):

        if i + 1 == len(LEVEL):
            if sample[i] == '0':
                cost -= 0.25
            elif sample[i] == '1':
                cost -= 1
            elif sample[i] == '2':
                cost += 0.5

        elif LEVEL[i + 1] == '_':
            if sample[i] == '0':
                cost -= 0.25
            elif sample[i] == '1' and sample[i + 1] != '1':
                cost += 0.5
            elif sample[i] == '1' and sample[i + 1] == '1':
                bad_indexes.append(i + 1)
            elif sample[i] == '2':
                cost += 0.5

        elif LEVEL[i + 1] == 'M':
            if sample[i] == '0':
                cost -= 2
            elif sample[i] == '1' and sample[i + 1] != '1':
                cost += 0.5
            elif sample[i] == '1' and sample[i + 1] == '1':
                bad_indexes.append(i + 1)
            elif sample[i] == '2':
                cost -= 1.5

        elif LEVEL[i + 1] == 'G':
            if sample[i] == '0':
                if i - 1 >= 0 and sample[i - 1] == '1':
                    cost -= 2
                else:
                    bad_indexes.append(i + 1)
            elif sample[i] == '1' and sample[i + 1] != '1':
                cost += 0
            elif sample[i] == '1' and sample[i + 1] == '1':
                bad_indexes.append(i + 1)
            elif sample[i] == '2':
                bad_indexes.append(i + 1)

        elif LEVEL[i + 1] == 'L':
            if sample[i] == '0':
                bad_indexes.append(i + 1)
            elif sample[i] == '1' and sample[i + 1] != '1':
                bad_indexes.append(i + 1)
            elif sample[i] == '1' and sample[i + 1] == '1':
                bad_indexes.append(i + 1)
            elif sample[i] == '2':
                if sample[i + 1] == '1':
                    bad_indexes.append(i + 1)
                else:
                    cost -= 0.25

    if len(bad_indexes) == 0:
        cost -= 5
        max_step = len(LEVEL)
    else:
        if len(bad_indexes) > 5:
            cost += 7
        elif len(bad_indexes) > 3:
            pass
        part_steps = list()
        for i in range(len(bad_indexes)):
            if i - 1 == 0:
                part_steps.append(len(LEVEL[0:bad_indexes[i]]))
            else:
                part_steps.append(len(LEVEL[bad_indexes[i - 1] + 1:bad_indexes[i]]))

        max_step = max(part_steps)

    fitness_value = max_step - cost

    FITNESS_MEMORY[sample] = fitness_value

    return FITNESS_MEMORY[sample]


def crossover(sample_x, sample_y):
    global LEVEL
    cross = random.randint(0, len(LEVEL) - 1)
    return sample_x[0:cross] + sample_y[cross:]


def mutate(sample):
    index = random.randint(0, len(LEVEL) - 1)
    new_sample = sample[:index]
    if sample[index] == '0':
        new_sample += random.choices(['1', '2'], weights=(0.5, 0.5), k=1)[0]
    elif sample[index] == '1':
        new_sample += random.choices(['0', '2'], weights=(0.82, 0.18), k=1)[0]
    else:
        new_sample += random.choices(['0', '1'], weights=(0.82, 0.18), k=1)[0]

    return new_sample + sample[index + 1:]


if __name__ == '__main__':
    LEVEL = input()
    pop, stats = genetic_algorithm()
    for j in pop:
        print(j)
    plt.plot(stats)
