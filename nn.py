import time
import random

# Created solely by Willoh

state = [ 0, 0, 0, 0]  # the first node will be the input node, and the last will be the output node

# a, b, c, d      a = index of the node to give, b = index of the node to recieve, c = mode of transfer (0: constant amount sent over if the giving node is positive, 1: fraction of giving node sent to recieving node, 2: contant amount given without subtraction from recieving node or check), d = magnitude of transfer
genes = [ [0, 1, 1, 0.5], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1],
         [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1],
         [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 3, 1, 1] ]
genes_m = []  # Genes of the mutant
mut_c = 0.25
it_C = 0
test_points = 5


best_fitness = 10000000


while True:
  
  genes_m = []
  for i in range(0, len(genes)):  # Cycles through the genes to create a mutant
    a = genes[i][0]
    r = random.uniform(0, 1)
    if(r < mut_c):
      a = random.randint(0, len(state) - 1)
    b = genes[i][1]
    r = random.uniform(0, 1)
    if(r < mut_c):
      b = random.randint(0, len(state) - 1)
    transfer_mode = genes[i][2]
    r = random.uniform(0, 1)
    if(r < mut_c):
      transfer_mode = random.randint(0, 2)
    magnitude = genes[i][3]
    r = random.uniform(0, 1)
    if(r < mut_c):
      magnitude = random.uniform(-1, 1) * 10 ** random.randint(-6, 1)
      if(magnitude < -2):
        magnitude = -1
      if(magnitude > 2):
        magnitude = 1
    genes_m.append([a, b, transfer_mode, magnitude])

  fitness = 0
  with open('data.txt', 'w') as file:
      file.write("")
  with open('gene.txt', 'w') as file:
      file.write(str(genes))
  for k in range(0, test_points):  # Tests the agent with various inputs and outputs
    x = k / 10
    y = x ** 2
    for j in range(0, len(state)):
      state[j] = 0
    state[0] = 1
    for i in range(0, len(genes)):  # Cycles through the genes to execute the instructions
      a = genes_m[i][0]
      b = genes_m[i][1]
      transfer_mode = genes_m[i][2]
      magnitude = genes_m[i][3]
      if(transfer_mode == 0):
        if(state[a] > 0):
          state[b] += magnitude
          state[a] -= magnitude
      elif(transfer_mode == 1):
        if(state[a] > 0):
          state[b] += magnitude * state[a]
          state[a] -= magnitude * state[a]
      elif(transfer_mode == 2):
        state[b] += magnitude
    result = state[-1]
    with open('data.txt', 'a') as file:
      file.write(str(x) + " " + str(y) + " " + str(result) + "\n")
    fitness += (y - result) ** 2 / (test_points + 1) * 10000
  if(fitness < best_fitness + 0.0001):
    best_fitness = fitness
    print("Iteration: " + str(it_C) + " Fitness: " + str(fitness))
    for i in range(0, len(genes)):  # Cycles through the genes to execute the instructions
      genes[i] = genes_m[i]
  it_C += 1
  time.sleep(0)
