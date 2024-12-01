import random
import matplotlib.pyplot as plt

def rule_to_dict(rule_number):
    binary = f"{rule_number:08b}"
    return {f"{a}{b}{c}": int(binary[7 - i]) for i, (a, b, c) in enumerate(
        [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
         (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    )}

def evolve(state, rule):
    n = len(state)
    new_state = state.copy()
    for i in range(n):
        left = state[(i - 1) % n]  # Wrap around edges
        center = state[i]
        right = state[(i + 1) % n]
        neighborhood = f"{left}{center}{right}"
        new_state[i] = rule[neighborhood]
    return new_state

def detect_pattern(state):
    # Detects the presence of clusters or isolated cells
    n = len(state)
    clusters = 0
    for i in range(n):
        if state[i] == 1 and state[(i + 1) % n] == 1:
            clusters += 1
    return clusters > 2  # If there are more than 2 clusters, we switch the rule

def simulate(rule_initial, rule_switch, steps, size=50, random_init=False):
    if random_init:
        state = [random.randint(0, 1) for _ in range(size)]
    else:
        state = [0] * size
        state[size // 2] = 1  # Single live cell in the middle

    rule_initial = rule_to_dict(rule_initial)
    rule_switch = rule_to_dict(rule_switch)

    history = [state]

    for i in range(steps):
        if detect_pattern(state):  # If a certain pattern is detected, switch rules
            state = evolve(state, rule_switch)
        else:
            state = evolve(state, rule_initial)
        history.append(state)

    return history

def plot_history(history, rule_initial, rule_switch, image_num):
    plt.figure(figsize=(10, 6))
    plt.imshow(history, cmap="tab20", interpolation="nearest")  # Colorful colormap (tab20)
    plt.title(f"Context-Aware Cellular Automaton - Output {image_num}\n"
              f"Initial Rule: {rule_initial}, Switch Rule: {rule_switch}")
    plt.xlabel("Cell Index")
    plt.ylabel("Time Step")
    plt.axis('off')  # Remove color bar and axes ticks
    plt.show()  # Show the plot

steps = 100  # Number of steps to simulate
size = 101  # Size of the grid
random_init = False  # Start with a single live cell or random grid

# Generate and plot 10 different outputs with random initial and switch rules
for i in range(1, 11):
    # Randomly choose both initial and switch rules from 0 to 255
    rule_initial = random.randint(0, 255)
    rule_switch = random.randint(0, 255)

    history = simulate(rule_initial, rule_switch, steps, size, random_init)
    plot_history(history, rule_initial, rule_switch, i)

print("10 images plotted successfully with random initial and switch rules.")
