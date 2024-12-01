import random
import matplotlib.pyplot as plt

def rule_to_dict(rule_number):
    binary = f"{rule_number:08b}"
    return {f"{a}{b}{c}": int(binary[7 - i]) for i, (a, b, c) in enumerate(
        [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
         (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    )}

def evolve(state, rule, update_frequency, step):
    n = len(state)
    new_state = state.copy()
    for i in range(n):
        # Cells update based on their individual time step
        if step % update_frequency[i] == 0:
            left = state[(i - 1) % n]  # Wrap around edges
            center = state[i]
            right = state[(i + 1) % n]
            neighborhood = f"{left}{center}{right}"
            new_state[i] = rule[neighborhood]
    return new_state

def simulate(rule, steps, size=50, random_init=False):
    if random_init:
        state = [random.randint(0, 1) for _ in range(size)]
    else:
        state = [0] * size
        state[size // 2] = 1  # Single live cell in the middle

    rule = rule_to_dict(rule)

    # Assign random update frequencies to each cell (between 1 and 5 steps)
    update_frequencies = [random.randint(1, 5) for _ in range(size)]

    history = [state]

    for i in range(steps):
        state = evolve(state, rule, update_frequencies, i)
        history.append(state)

    return history

def plot_history(history, rule_number, image_num):
    plt.figure(figsize=(10, 6))
    plt.imshow(history, cmap="tab20", interpolation="nearest")  # Colorful colormap (tab20)
    plt.title(f"Rule {rule_number} - Spatially Varying Update Frequency Cellular Automaton - Output {image_num}")
    plt.xlabel("Cell Index")
    plt.ylabel("Time Step")
    plt.axis('off')  # Remove axis ticks
    plt.show()  # Show the plot

steps = 100  # Number of steps to simulate
size = 101  # Size of the grid
random_init = False  # Start with a single live cell or random grid

# Generate and plot 10 different outputs with random initial rules
for i in range(255):
    # Randomly choose initial rule from 0 to 255
    rule_number = random.randint(0, 255)

    history = simulate(i, steps, size, random_init)
    plot_history(history, i, i)

print("10 images plotted successfully with random rules and update frequencies.")
