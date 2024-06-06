import time
import random

# Created solely by Willoh

state = [ 0, 0, 0, 0]  # the first node will be the input node, and the last will be the output node

# a, b, c, d      a = index of the node to give, b = index of the node to recieve, c = mode of transfer (0: constant amount sent over if the giving node is positive, 1: fraction of giving node sent to recieving node), d = magnitude of transfer
genes = [ [0, 1, 1, 0.5], [1, 2, 1, 1], [2, 3, 1, 1] ]


best_fitness = 10000000


while True:
  fitness = 0
  for i in range(0, len(genes)):
    a = genes[i][0]
    b = genes[i][1]
    transfer_mode = genes[i][2]
    magnitude = genes[i][3]
    if(transfer_mode == 0):
      if(state[a] > 0):
        state[b] += magnitude
    elif(transfer_mode == 1):
      if(state[a] > 0):
        state[b] += magnitude * state[a]
  result = state[-1]
  print(str(result))
  time.sleep(10)
