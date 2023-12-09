import random
import copy
import matplotlib.pyplot as plt
import math

N = 20
MIN = -10
MAX = 10

P = 1000
MUTRATE = 0.4
MUTSTEP = 0.8
G = 1000


class individual:
    def __init__(self):
        self.gene = [0] * N
        self.fitness = 0


population = []

for x in range(0, P):
    tempgene = []
    for y in range(0, N):
        tempgene.append(random.uniform(MIN, MAX))
    newind = individual()
    newind.gene = tempgene.copy()
    population.append(newind)


def test_function2(ind):
    utility = 0
    for i in range(0, N):
        utility += (ind.gene[i] * ind.gene[i]) - 10 * math.cos((2 * math.pi) * ind.gene[i])
    return utility + 10 * N


def test_function(ind):
    utility = ((ind.gene[0] - 1) * (ind.gene[0] - 1))
    for i in range(1, N):
        utility = utility + (i * (((2 * (ind.gene[i] ** 2)) - ind.gene[i - 1]) ** 2))
    return utility


def test_function1(ind):
    utility1 = 0

    utility2 = 0

    for i in range(N):
        utility1 = utility1 + (ind.gene[i] ** 2)

        utility2 = utility2 + (0.5 * (i + 1) * ind.gene[i])

    return (utility1 + (utility2 ** 2) + (utility2 ** 4))


totalint = 0

for ind in population:
    ind.fitness = test_function(ind)
    totalint += ind.fitness

generations = []
mean_fitnesses = []
best_fitnesses = []

for x in range(0, G):

    offspring = []

    for i in range(0, P):
        parent1 = random.randint(0, P - 1)
        off1 = copy.deepcopy(population[parent1])
        parent2 = random.randint(0, P - 1)
        off2 = copy.deepcopy(population[parent2])
        if off1.fitness < off2.fitness:
            offspring.append(off1)
        else:
            offspring.append(off2)

    toff1 = individual()
    toff2 = individual()
    temp = individual()

    for i in range(0, P, 2):

        toff1 = copy.deepcopy(offspring[i])
        toff2 = copy.deepcopy(offspring[i + 1])
        temp = copy.deepcopy(offspring[i])
        crosspoint = random.randint(1, N)

        for j in range(crosspoint, N):
            toff1.gene[j] = toff2.gene[j]
            toff2.gene[j] = temp.gene[j]
        offspring[i] = copy.deepcopy(toff1)
        offspring[i + 1] = copy.deepcopy(toff2)

    for i in range(0, P):
        newind = individual()
        newind.gene = []
        for j in range(0, N):
            gene = offspring[i].gene[j]
            mutprob = random.random()
            if mutprob < MUTRATE:
                alter = random.uniform(-MUTSTEP, MUTSTEP)
                gene = gene + alter
                if gene > MAX:
                    gene = MAX
                if gene < MIN:
                    gene = MIN
            newind.gene.append(gene)
        offspring[i] = copy.deepcopy(newind)

    for off in offspring:
        off.fitness = test_function(off)

    for i in range(0, P):
        if offspring[i].fitness > population[i].fitness:
            offspring[i] = copy.deepcopy(population[i])

    bestind = population[0]
    for i in range(0, P):
        if population[i].fitness < bestind.fitness:
            bestind = population[i]
    population = copy.deepcopy(offspring)

    worstind = population[0]
    worstpos = 0
    for i in range(0, P):
        if population[i].fitness > worstind.fitness:
            worstind = population[i]
            worstpos = i
    population[worstpos] = bestind

    totaloff = 0
    for off in offspring:
        off.fitness = test_function(off)
        totaloff += off.fitness

    generations.append(x + 1)
    mean_fitnesses.append(totaloff / P)
    best_fitnesses.append(min(off.fitness for off in population))

    # print(totaloff)
    print(bestind.fitness, worstind.fitness)
    print(mean_fitnesses)

plt.plot(generations, mean_fitnesses, label="Mean fitness")
plt.plot(generations, best_fitnesses, label="Min fitness")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()
plt.grid(True)
plt.show()
