import time
import random

state = [0, 0, 0, 0]  # the first node will be the input node, and the last will be the output node.

# a, b, c, d      a = index of the node to give, b = index of the node to receive, c = mode of transfer (0: constant amount sent over if the giving node is positive, 1: fraction of giving node sent to receiving node, 2: constant amount given without subtraction from receiving node or check), d = magnitude of transfer
genes = [[0, 1, 1, 0.5], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 3, 1, 1]]
genes_m = []  # Genes of the mutant
mut_c = 0.25
it_C = 0
test_points = 50

best_fitness = 10000000

def test_agent(genes_in, state_in):
    fitness_a = 0
    with open('data.txt', 'w') as file:
        file.write("")
    with open('gene.txt', 'w') as file:
        file.write(str(genes_in))
    for k in range(0, test_points):  # Tests the agent with various inputs and outputs
        x = k / test_points
        y = x ** 2
        for j in range(0, len(state_in)):
            state_in[j] = 0
        state_in[0] = x
        for i in range(0, len(genes_in)):  # Cycles through the genes to execute the instructions
            a = genes_in[i][0]
            b = genes_in[i][1]
            transfer_mode = genes_in[i][2]
            magnitude = genes_in[i][3]
            if transfer_mode == 0:
                if state_in[a] > 0:
                    state_in[b] += magnitude
                    state_in[a] -= magnitude
            elif transfer_mode == 1:
                if state_in[a] > 0:
                    state_in[b] += magnitude * state_in[a]
                    state_in[a] -= magnitude * state_in[a]
            elif transfer_mode == 2:
                state_in[b] += magnitude
        result = state_in[-1]
        with open('data.txt', 'a') as file:
            file.write(str(x) + " " + str(y) + " " + str(result) + "\n")
        fitness_a += (y - result) ** 2 / (test_points + 1) * 10000
    return fitness_a

def mutate_agent(genes_in):
    genes_out = []
    for i in range(0, len(genes_in)):  # Cycles through the genes to create a mutant
        a = genes_in[i][0]
        r = random.uniform(0, 1)
        if r < mut_c:
            a = random.randint(0, len(state) - 1)
        b = genes_in[i][1]
        r = random.uniform(0, 1)
        if r < mut_c:
            b = random.randint(0, len(state) - 1)
        transfer_mode = genes_in[i][2]
        r = random.uniform(0, 1)
        if r < mut_c:
            transfer_mode = random.randint(0, 2)
        magnitude = genes_in[i][3]
        r = random.uniform(0, 1)
        if r < mut_c:
            magnitude = random.uniform(-1, 1) * 10 ** random.randint(-6, 1)
            if magnitude < -2:
                magnitude = -1
            if magnitude > 2:
                magnitude = 1
        genes_out.append([a, b, transfer_mode, magnitude])
    return genes_out


while True:
    genes_m = mutate_agent(genes)
    


    fitness = test_agent(genes_m, state)

    
    if fitness <= best_fitness:
        best_fitness = fitness
        print("Iteration: " + str(it_C) + " Fitness: " + str(fitness))
        for i in range(0, len(genes)):  # Cycles through the genes to execute the instructions
            genes[i] = genes_m[i]
    it_C += 1
    time.sleep(0.01)