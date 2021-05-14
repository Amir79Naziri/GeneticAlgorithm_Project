import random

CHROMOSOME_NUMBER = 200
LEVEL = ''
FITNESS_MEMORY = dict()


def population_generator(population_number):
    global CHROMOSOME_NUMBER
    initial_population = list()
    for _ in range(CHROMOSOME_NUMBER):
        sample = list()
        for _ in range(population_number):
            random_number = random.random()
            if random_number <= 0.7:
                sample.append(0)
            elif 0.7 < random_number <= 0.85:
                sample.append(1)
            else:
                sample.append(2)

        initial_population.append(sample)

    return initial_population


def random_selection(population, fitness_func):
    weights = list()
    fitness_values = list()
    total_sum = 0

    for sample in population:
        value = fitness_func(sample)
        fitness_values.append(value)
        total_sum += value

    for value in fitness_values:
        weights.append(value / total_sum)

    return random.choices(population=population, weights=weights, k=1)


def fitness_function(sample):
    global FITNESS_MEMORY
    if sample in FITNESS_MEMORY:
        return FITNESS_MEMORY[sample]

    steps = 0
    for i in range(len(sample)):
        current_action = sample[i]

        if i + 1 == len(sample):
            steps += 1

        elif current_action == '0':
            if LEVEL[i + 1] == '_':
                steps += 1
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
            elif LEVEL[i + 1] == 'M':
                steps += 1
            else:
                break

    if steps == len(LEVEL):
        steps += 3

    FITNESS_MEMORY[sample] = steps

    return FITNESS_MEMORY[sample]


if __name__ == '__main__':
    LEVEL = input()
