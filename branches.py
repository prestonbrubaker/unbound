import time
import random
import pygame
import math
pygame.init()

# Contants for Pygame
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
BAR_WIDTH = 3
BAR_COLOR = (0, 128, 255)
BACKGROUND_COLOR = (255, 255, 255)
ACTUAL_COLOR = (255, 0, 0)
GUESSED_COLOR = (0, 255, 0)

# Create Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fitness Histogram')



state = [0, 0, 0, 0]  # the first node will be the input node, and the last will be the output node.

# a, b, c, d      a = index of the node to give, b = index of the node to receive, c = mode of transfer (0: constant amount sent over if the giving node is positive, 1: fraction of giving node sent to receiving node, 2: constant amount given without subtraction from receiving node or check), d = magnitude of transfer
genes = [[0, 1, 1, 0.5], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 3, 1, 1]]
genes_m = []  # Genes of the mutant
mut_c = 0.09
it_C = 0
test_points = 500
agent_list = []
agent_fitness_list = []
agent_count = 1000
best_fitness = 10000000
guess_x = []
guess_y = []
guess_g = []




# Function to draw the histogram and graph
def draw(fitness_values, guess_x, guess_y, guess_g):
    for i in range(len(fitness_values)):
        fitness_values[i] = math.log(fitness_values[i])
    screen.fill(BACKGROUND_COLOR)
    
    # Draw Histogram on the left side
    max_fitness = max(fitness_values) if fitness_values else 1
    num_bars = min(len(fitness_values), SCREEN_WIDTH // (2 * BAR_WIDTH))
    
    for i in range(num_bars):
        fitness = fitness_values[-(i+1)]  # Start from the end (highest fitness)
        bar_height = (fitness / max_fitness) * SCREEN_HEIGHT
        x = (SCREEN_WIDTH // 2) - (i + 1) * BAR_WIDTH
        pygame.draw.rect(screen, BAR_COLOR, (x, SCREEN_HEIGHT - bar_height, BAR_WIDTH, bar_height))
    
    # Draw Graph on the right side
    graph_width = SCREEN_WIDTH // 2
    graph_height = SCREEN_HEIGHT
    for i in range(len(guess_x) - 1):
        actual_start = (graph_width + int(guess_x[i] * graph_width), graph_height - int(guess_y[i] * graph_height))
        actual_end = (graph_width + int(guess_x[i + 1] * graph_width), graph_height - int(guess_y[i + 1] * graph_height))
        guessed_start = (graph_width + int(guess_x[i] * graph_width), graph_height - int(guess_g[i] * graph_height))
        guessed_end = (graph_width + int(guess_x[i + 1] * graph_width), graph_height - int(guess_g[i + 1] * graph_height))
        
        pygame.draw.line(screen, ACTUAL_COLOR, actual_start, actual_end, 2)
        pygame.draw.line(screen, GUESSED_COLOR, guessed_start, guessed_end, 2)
    
    pygame.display.flip()

def initialize_population():
    agent_list_out = []
    for i in range(0, agent_count):
        agent_list_out.append(genes)
    return agent_list_out

def initialize_fitness_list():
    agent_fitness_list_out = []
    for i in range(0, agent_count):
        agent_fitness_list_out.append(0)
    return agent_fitness_list_out



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

def run_agent(genes_in, state_in):
    guess_x_out = []
    guess_y_out = []
    guess_g_out = []
    for k in range(0, test_points):  # Tests the agent with various inputs and outputs
        x = k / test_points
        guess_x_out.append(x)
        y = x ** 2
        guess_y_out.append(y)
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
        guess_g_out.append(result)
    return guess_x_out, guess_y_out, guess_g_out

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
            magnitude = random.uniform(-1, 1) * 10 ** random.randint(-8, 0)
            if magnitude < -2:
                magnitude = -1
            if magnitude > 2:
                magnitude = 1
        genes_out.append([a, b, transfer_mode, magnitude])
    return genes_out







# Initialization
agent_list = initialize_population()
agent_fitness_list = initialize_fitness_list()




while True:
    genes_m = mutate_agent(genes)
    fitness = test_agent(genes_m, state)

    # Test all of the agents to get their fitness values
    for n in range(0, agent_count):
        agent_fitness_list[n] = test_agent(agent_list[n], state)
    
    # Sort the agents by their fitness values
    combined = list(zip(agent_fitness_list, agent_list))
    combined = sorted(combined, key=lambda x: x[0])
    agent_fitness_list, agent_list = zip(*combined)
    agent_fitness_list = list(agent_fitness_list)
    agent_list = list(agent_list)


    # Draw the histogram
    guess_x, guess_y, guess_g = run_agent(agent_list[0], state)
    draw(agent_fitness_list, guess_x, guess_y, guess_g)


    # Replace the highest fitness agents with mutated versions of the lowest fitness agents
    for n in range(0, int(agent_count / 2)):
        agent_list[-1 * (n + 1)] = mutate_agent(agent_list[n])
    

    


    print(agent_fitness_list[0])
    it_C += 1
    time.sleep(0.01)