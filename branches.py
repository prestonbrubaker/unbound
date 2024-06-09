import time
import random
import pygame
import math
import statistics
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

# a, b, c, d      a = index of the node to give, b = index of the node to receive, c = mode of transfer (0: constant amount sent over if the giving node is positive, 1: fraction of giving node sent to receiving node, 2: constant amount given without subtraction from receiving node or check), d = magnitude of transfer
genes = [[0, 1, 1, 0.5], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 2, 1, 1], [2, 3, 1, 1], [3, 4, 1, 1], [4, 5, 1, 1], [5, 6, 1, 1], [6, 7, 1, 1], [7, 8, 1, 1]]
genes_m = []  # Genes of the mutant
mut_c = 0.005
it_C = 0
test_points = 100
agent_list = []             # List containing the genes/instructions for each agent
agent_state_count_list = [] # List containing the number of nodes each agent has
agent_fitness_list = []     # List containing the fitness of each agent
agent_count = 1000
best_fitness = 10000000
guess_x = []
guess_y = []
guess_g = []
best_fitness_log = []




# Function to draw the histogram, graph, and fitness log
def draw(fitness_values, guess_x, guess_y, guess_g, fitness_log, it_C, best_fitness, agent_state_count_list_in, gene_length_list_in):
    for i in range(len(fitness_values)):
        fitness_values[i] = math.log(fitness_values[i])
    screen.fill(BACKGROUND_COLOR)
    
    # Draw Histogram on the left side (1/3 of the screen)
    max_fitness = max(fitness_values) if fitness_values else 1
    num_bars = min(len(fitness_values), (SCREEN_WIDTH // 3) // BAR_WIDTH)
    
    for i in range(num_bars):
        fitness = fitness_values[-(i+1)]  # Start from the end (highest fitness)
        bar_height = (fitness / max_fitness) * SCREEN_HEIGHT
        x = (SCREEN_WIDTH // 3) - (i + 1) * BAR_WIDTH
        pygame.draw.rect(screen, BAR_COLOR, (x, SCREEN_HEIGHT - bar_height, BAR_WIDTH, bar_height))
    
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

def test_agent(genes_in, state_c_in):
    fitness_a = 0
    #with open('data.txt', 'w') as file:
    #    file.write("")
    #with open('gene.txt', 'w') as file:
    #    file.write(str(genes_in))
    state_in = []
    for i in range(0, state_c_in):
        state_in.append(0)
    for k in range(0, test_points):  # Tests the agent with various inputs and outputs
        for i in range(0, state_c_in):
            state_in[i] = 0
        x = k / test_points
        y = x ** 2
        state_in[0] = x
        for i in range(0, len(genes_in)):  # Cycles through the genes to execute the instructions
            a = genes_in[i][0]
            if(a > state_c_in - 1):
                a = state_c_in - 1
            b = genes_in[i][1]
            if(b > state_c_in - 1):
                b = state_c_in - 1
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
        #with open('data.txt', 'a') as file:
        #    file.write(str(x) + " " + str(y) + " " + str(result) + "\n")
        fitness_a += (((y - result) ** 2) * 10000) / test_points
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
        y = x ** 2
        guess_y_out.append(y)
        state_in[0] = x
        for i in range(0, len(genes_in)):  # Cycles through the genes to execute the instructions
            a = genes_in[i][0]
            if(a > state_c_in - 1):
                a = state_c_in - 1
            b = genes_in[i][1]
            if(b > state_c_in - 1):
                b = state_c_in - 1
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

def mutate_agent(genes_in, agent_state_count_in):
    genes_out = []
    agent_state_count_out = agent_state_count_in
    mut_c_m = random.uniform(0, 1)
    max_mag = random.randint(-9, 0)
    for i in range(0, len(genes_in)):  # Cycles through the genes to create a mutant
        a = genes_in[i][0]
        r = random.uniform(0, 1)
        if r < mut_c * mut_c_m:
            a = random.randint(0, len(state) - 1)
        b = genes_in[i][1]
        r = random.uniform(0, 1)
        if r < mut_c * mut_c_m:
            b = random.randint(0, len(state) - 1)
        transfer_mode = genes_in[i][2]
        r = random.uniform(0, 1)
        if r < mut_c * mut_c_m:
            transfer_mode = random.randint(0, 2)
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
        genes_in.insert(random.randint(0, len(genes_in) - 1), genes_in[random.randint(0, len(genes_in) - 1)])
    r = random.uniform(0, 1)
    if r < mut_c * mut_c_m:
        genes_in.pop(random.randint(0, len(genes_in) - 1))
    r = random.uniform(0, 1)
    r = random.uniform(0, 1)
    if r < mut_c * mut_c_m:
        genes_in.pop(len(genes_in) - 1)
    r = random.uniform(0, 1)
    if r < mut_c * mut_c_m:
        genes_in.append(genes_in[random.randint(0, len(genes_in) - 1)])
    r = random.uniform(0, 1)
    if r < mut_c * mut_c_m:
        agent_state_count_out += random.randint(-1, 1)
        if(agent_state_count_out < 1):
            agent_state_count_out = 1
    
    return genes_out, agent_state_count_out

def save_state_and_genes(state_in, genes_in, filename='state_genes.json'):
    data = {
        'states_in': state_in,
        'genes_in': genes_in
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"State and genes saved to {os.path.abspath(filename)}")






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


    # Draw
    guess_x, guess_y, guess_g = run_agent(agent_list[0], agent_state_count_list[0])
    gene_length_list = []

    save_state_and_genes(agent_state_count_list[0], agent_list[0])

    for i in range(0, len(agent_list)):
        gene_length_list.append(len(agent_list[i]))
    draw(agent_fitness_list, guess_x, guess_y, guess_g, best_fitness_log, it_C, agent_fitness_list[0], agent_state_count_list, gene_length_list)

    print(agent_fitness_list[0])
    if(agent_fitness_list[0] > 0):
        best_fitness_log.append(math.log(agent_fitness_list[0]))
    else:
        best_fitness_log.append(0)
    if(len(best_fitness_log) > 2000):
        for i in range(0, int(len(best_fitness_log) / 2)):
            best_fitness_log.pop(-i * 2 + 1)
    
    # Replace the highest fitness agents with mutated versions of the lowest fitness agents
    agent_fitness_list = initialize_fitness_list()
    for n in range(0, int(4 * agent_count / 5)):
        r = random.uniform(0, 1)
        if(r < 0.85):
            index = random.randint(0, int(agent_count / 5))
            agent_list[-1 * (n + 1)], agent_state_count_list[-1 * (n + 1)] = mutate_agent(agent_list[index], agent_state_count_list[index])
        else:
            r = random.uniform(0, 1)
            if(r < 0.75):
                agent_list[-1 * (n + 1)], agent_state_count_list[-1 * (n + 1)] = mutate_agent(agent_list[-1 * (n + 1)], agent_state_count_list[-1 * (n + 1)])
    
    it_C += 1
    time.sleep(0.01)
