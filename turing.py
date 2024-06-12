import time
import random
import pygame
import math
import statistics
import json
import os

pygame.init()

# Contants for Pygame
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 950
BAR_WIDTH = 3
BAR_COLOR = (0, 128, 255)
BACKGROUND_COLOR = (255, 255, 255)
ACTUAL_COLOR_INSIDE = (255, 0, 0)
ACTUAL_COLOR_OUTSIDE = (0, 0, 255)
GUESSED_COLOR = (0, 255, 0)
LOG_COLOR = (0, 0, 0)
FONT_SIZE = 24
MARGIN_RATIO = 0.1  # 10% margin

# Create Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fitness Histogram')
font = pygame.font.Font(None, FONT_SIZE)


state = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # the first node will be the input node, and the last will be the output node.

# a, b, c, d      a = index of the node to give, b = index of the node to receive, c = mode of transfer (0: constant amount sent over if the giving node is positive, 1: fraction of giving node sent to receiving node, 2: constant amount given without subtraction from receiving node or check, 3: sine of node a is taken to be node b), d = magnitude of transfer
genes = [[0, 1, 1, 0.5], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 3, 1, 1], [3, 4, 1, 1], [4, 5, 1, 1], [5, 6, 1, 1], [6, 7, 1, 1], [7, 8, 1, 1]]
genes_m = []  # Genes of the mutant
mut_c = .9
it_C = 0
test_points = 100
agent_list = []             # List containing the genes/instructions for each agent
agent_state_count_list = [] # List containing the number of nodes each agent has
agent_fitness_list = []     # List containing the fitness of each agent
agent_count = 500
best_fitness = 10000000
guess_x = []
guess_y = []
guess_g = []
best_fitness_log = []




# Function to draw the histogram, graph, and fitness log
def draw(fitness_values, guess_x, guess_y, guess_g, fitness_log, it_C, best_fitness, agent_state_count_list_in, gene_length_list_in):
    log_fitness_values = []
    for i in range(len(fitness_values)):
        log_fitness_values.append(math.log(fitness_values[i]))
    screen.fill(BACKGROUND_COLOR)
    
    # Draw Histogram on the left side (1/3 of the screen)
    if log_fitness_values:
        max_log_fitness = max(log_fitness_values)
        min_log_fitness = min(log_fitness_values)
    else:
        max_log_fitness = 1
        min_log_fitness = 0
        
    range_log_fitness = max_log_fitness - min_log_fitness if max_log_fitness != min_log_fitness else 1
    num_bars = min(len(log_fitness_values), (SCREEN_WIDTH // 3) // BAR_WIDTH)
    red_threshold = int(num_bars * 0.1)
    
    for i in range(num_bars):
        log_fitness = log_fitness_values[-(i+1)]  # Start from the end (highest fitness)
        normalized_fitness = (log_fitness - min_log_fitness) / range_log_fitness
        bar_height = normalized_fitness * SCREEN_HEIGHT
        x = (SCREEN_WIDTH // 3) - (i + 1) * BAR_WIDTH
        bar_color = (255, 0, 0) if i > num_bars - red_threshold else BAR_COLOR
        pygame.draw.rect(screen, bar_color, (x, SCREEN_HEIGHT - bar_height, BAR_WIDTH, bar_height))
    
    # Draw Graph in the middle part (1/3 of the screen)
    graph_width = SCREEN_WIDTH // 3
    graph_height = SCREEN_HEIGHT
    margin = SCREEN_HEIGHT * MARGIN_RATIO
    for i in range(len(guess_x) - 1):
        actual_start = (SCREEN_WIDTH // 3 + int((guess_x[i] / 1.2 + 0.1) * graph_width), graph_height - int(guess_y[i] * graph_height))
        actual_end = (SCREEN_WIDTH // 3 + int((guess_x[i + 1] / 1.2 + 0.1) * graph_width), graph_height - int(guess_y[i + 1] * graph_height))
        guessed_start = (SCREEN_WIDTH // 3 + int((guess_x[i] / 1.2 + 0.1) * graph_width), graph_height - int(guess_g[i] * graph_height))
        guessed_end = (SCREEN_WIDTH // 3 + int((guess_x[i + 1] / 1.2 + 0.1) * graph_width), graph_height - int(guess_g[i + 1] * graph_height))
        if(guess_x[i] >= 0 and guess_x[i + 1] <= 1):
            pygame.draw.line(screen, ACTUAL_COLOR_INSIDE, actual_start, actual_end, 2)
        else:
            pygame.draw.line(screen, ACTUAL_COLOR_OUTSIDE, actual_start, actual_end, 2)
        pygame.draw.line(screen, GUESSED_COLOR, guessed_start, guessed_end, 2)
    
    # Draw Fitness Log on the right side (1/3 of the screen) with margin
    if fitness_log:
        min_log = min(fitness_log)
        max_log = max(fitness_log)
        log_range = max_log - min_log if max_log - min_log != 0 else 1

        margin = SCREEN_HEIGHT * MARGIN_RATIO
        log_height = SCREEN_HEIGHT - 2 * margin
        log_width = SCREEN_WIDTH // 3

        for i in range(len(fitness_log) - 1):
            log_start = (2 * SCREEN_WIDTH // 3 + int(i / len(fitness_log) * log_width), SCREEN_HEIGHT - margin - int((fitness_log[i] - min_log) / log_range * log_height))
            log_end = (2 * SCREEN_WIDTH // 3 + int((i + 1) / len(fitness_log) * log_width), SCREEN_HEIGHT - margin - int((fitness_log[i + 1] - min_log) / log_range * log_height))
            pygame.draw.line(screen, LOG_COLOR, log_start, log_end, 2)

    # Display iteration count and best fitness
    text_surface1 = font.render(f"Iteration: {it_C}", True, LOG_COLOR)
    screen.blit(text_surface1, (10, 10))
    text_surface2 = font.render(f"Best Fitness: {best_fitness:.6f}", True, LOG_COLOR)
    screen.blit(text_surface2, (10, 10 + FONT_SIZE))
    text_surface2 = font.render(f"Average # of Nodes: {statistics.mean(agent_state_count_list_in):.6f}", True, LOG_COLOR)
    screen.blit(text_surface2, (10, 10 + 2 * FONT_SIZE))
    text_surface2 = font.render(f"Average # of Genes: {statistics.mean(gene_length_list_in):.6f}", True, LOG_COLOR)
    screen.blit(text_surface2, (10, 10 + 3 * FONT_SIZE))

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

def initialize_agent_state_count():
    agent_state_count_list_out = []
    for i in range(0, agent_count):
        agent_state_count_list_out.append(len(state))
    return agent_state_count_list_out

def evaluate_agent(x_in, genes_inn, state_inn):
    state_inn[0] = x_in
    i = 0
    while(i < len(genes_inn)):  # Runs through the genes to execute the instructions
        a = genes_inn[i][0]
        if(a > len(state_inn) - 1):
            a = len(state_inn) - 1
        b = genes_inn[i][1]
        if(b > len(state_inn) - 1):
            b = len(state_inn) - 1
        transfer_mode = genes_inn[i][2]
        magnitude = genes_inn[i][3]
        if transfer_mode == 0:
            if state_inn[a] > 0:
                state_inn[b] += magnitude
                state_inn[a] -= magnitude
        elif transfer_mode == 1:
            if state_inn[a] > 0:
                state_inn[b] += magnitude * state_inn[a]
                state_inn[a] -= magnitude * state_inn[a]
        elif transfer_mode == 2:
            state_inn[b] += magnitude
        elif transfer_mode == 3:
            if(state_inn[a] > 0):
                state_inn[b] += math.sin(state_inn[a])
                state_inn[a] -= math.sin(state_inn[a])
        i += 1
    result = state_inn[-1]
    return result

def test_agent(genes_in, state_c_in):
    fitness_a = 0
    state_in = []
    for i in range(0, state_c_in):
        state_in.append(0)
    for k in range(0, test_points):  # Tests the agent with various inputs and outputs
        for i in range(0, state_c_in):
            state_in[i] = 0
        x = k / test_points
        y = math.sin(x * 2 * 3.142) / 2 + 0.5
        result = evaluate_agent(x, genes_in, state_in)
        se = (y - result)**2
        fitness_a += se
    return fitness_a

def run_agent(genes_in, state_c_in):
    guess_x_out = []
    guess_y_out = []
    guess_g_out = []
    state_in = []
    for i in range(0, state_c_in):
        state_in.append(0)
    for k in range(0, test_points):  # Tests the agent with various inputs and outputs
        for i in range(0, state_c_in):
            state_in[i] = 0
        x = k / test_points * 1.2 - 0.1
        guess_x_out.append(x)
        y = math.sin(x * 2 * 3.142) / 2 + 0.5
        guess_y_out.append(y)
        result = evaluate_agent(x, genes_in, state_in)
        guess_g_out.append(result)
    return guess_x_out, guess_y_out, guess_g_out

def mutate_agent(genes_in, agent_state_count_in):
    genes_out = []
    agent_state_count_out = agent_state_count_in
    mut_c_m = random.uniform(0, 1)
    max_mag = random.randint(-9, 0)
    for i in range(0, len(genes_in)):  # Cycles through the genes to create a mutant
        a = genes_in[i][0]
        r = random.uniform(0, 1)
        if r < mut_c * mut_c_m:
            a = random.randint(0, agent_state_count_in - 1)
        b = genes_in[i][1]
        r = random.uniform(0, 1)
        if r < mut_c * mut_c_m:
            b = random.randint(0, agent_state_count_in - 1)
        transfer_mode = genes_in[i][2]
        r = random.uniform(0, 1)
        if r < mut_c * mut_c_m:
            transfer_mode = random.randint(0, 3)
        magnitude = genes_in[i][3]
        r = random.uniform(0, 1)
        if r < mut_c * mut_c_m:
            magnitude = random.uniform(-1, 1) * 10 ** random.randint(-9, max_mag)
            if magnitude < -2:
                magnitude = -1
            if magnitude > 2:
                magnitude = 1
        genes_out.append([a, b, transfer_mode, magnitude])
    r = random.uniform(0, 1)
    if r < mut_c * mut_c_m:
        ridx = random.randint(0, len(genes_out) - 1)
        if(ridx < len(genes_out)):
            genes_out.insert(ridx, genes_in[random.randint(0, len(genes_in) - 1)])
    r = random.uniform(0, 1)
    if r < mut_c * mut_c_m and len(genes_out) > 1:
        genes_out.pop(random.randint(0, len(genes_out) - 1))
    r = random.uniform(0, 1)
    if r < mut_c * mut_c_m and len(genes_out) > 1:
        genes_out.pop(len(genes_out) - 1)
    r = random.uniform(0, 1)
    if r < mut_c * mut_c_m:
        genes_out.append(genes_in[random.randint(0, len(genes_in) - 1)])
    r = random.uniform(0, 1)
    if r < mut_c * mut_c_m:
        agent_state_count_out += random.randint(-1, 1)
        if(agent_state_count_out < 1):
            agent_state_count_out = 1
    
    return genes_out, agent_state_count_out




# Initialization
agent_list = initialize_population()
agent_fitness_list = initialize_fitness_list()
agent_state_count_list = initialize_agent_state_count()




while True:

    # Test all of the agents to get their fitness values
    agent_fitness_list = initialize_fitness_list()
    for n in range(0, agent_count):
        agent_fitness_list[n] = test_agent(agent_list[n], agent_state_count_list[n])
    
    # Sort the agents by their fitness values
    combined = list(zip(agent_fitness_list, agent_list, agent_state_count_list))
    combined = sorted(combined, key=lambda x: x[0])
    agent_fitness_list, agent_list, agent_state_count_list = zip(*combined)
    agent_fitness_list = list(agent_fitness_list)
    agent_list = list(agent_list)
    agent_state_count_list = list(agent_state_count_list)


    print(agent_fitness_list[0])

    # Draw
    guess_x, guess_y, guess_g = run_agent(agent_list[0], agent_state_count_list[0])
    gene_length_list = []

    for i in range(0, len(agent_list)):
        gene_length_list.append(len(agent_list[i]))
    draw(agent_fitness_list, guess_x, guess_y, guess_g, best_fitness_log, it_C, agent_fitness_list[0], agent_state_count_list, gene_length_list)

    
    if(agent_fitness_list[0] > 0):
        best_fitness_log.append(math.log(agent_fitness_list[0]))
    else:
        best_fitness_log.append(0)
    
    # Replace the highest fitness agents with mutated versions of the lowest fitness agents
    for n in range(int(0.2 * agent_count), agent_count):
        r = random.uniform(0, 1)
        if(r < 0.85):
            index = random.randint(0, int(agent_count * .2))
            agent_list[n], agent_state_count_list[n] = mutate_agent(agent_list[index], agent_state_count_list[index])
        else:
            agent_list[n], agent_state_count_list[n] = mutate_agent(agent_list[n], agent_state_count_list[n])
    
    it_C += 1
    time.sleep(0.01)
