import random
import numpy as np

CHROMOSOME_NUMBER = 200
LEVEL = '____G_ML__G_'
FITNESS_MEMORY = dict()


def genetic_algorithm():
    population = population_generator()
    while not is_convergent(population):
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
    return population


def is_convergent(population, limit=0.05):
    weights = [fitness_function(_) for _ in population]
    if np.sqrt(np.var(np.array(weights))) > limit:
        return False
    else:
        return True


def population_generator():
    global CHROMOSOME_NUMBER
    initial_population = list()
    for _ in range(CHROMOSOME_NUMBER):
        sample = ''
        for _ in range(len(LEVEL)):
            random_number = random.random()
            if random_number <= 0.7:
                sample += '0'
            elif 0.7 < random_number <= 0.85:
                sample += '1'
            else:
                sample += '2'

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

    steps = 0
    for i in range(len(LEVEL)):
        current_action = sample[i]

        if i + 1 == len(LEVEL):
            steps += 1

        elif current_action == '0':
            if LEVEL[i + 1] == '_':
                steps += 1
            elif LEVEL[i + 1] == 'M':
                steps += 2
            else:
                break

        elif current_action == '1':
            if LEVEL[i + 1] == '_':
                steps += 1
            elif LEVEL[i + 1] == 'G':
                steps += 1
            else:
                break

        elif current_action == '2':
            if LEVEL[i + 1] == '_':
                steps += 1
            elif LEVEL[i + 1] == 'L':
                steps += 1
            else:
                break

    if steps == len(LEVEL):
        steps += 7

    FITNESS_MEMORY[sample] = steps

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
    # LEVEL = input()
    pop = genetic_algorithm()
    for j in pop:
        print(j)