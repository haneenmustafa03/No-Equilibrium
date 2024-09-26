# Simulation Params (Can be tweaked for increase/decrease tax cheating)
BASE_MAX_CATCH_PROB = 0.5        # Base maximum probability of catching an individual
UTILITY_PER_PERCENT = 1          # Utility gained per percent of tax skipped
LEARNING_RATE_IF_CAUGHT = 0.2    # Learning rate adjustment if caught
LEARNING_RATE_IF_NOT_CAUGHT = 0.05
SCRUTINY_MULTIPLIER = 3.0        # Multiplier for catch probability during scrutiny
SCRUTINY_DURATION = 4            # Number of rounds an individual is under scrutiny
MAX_TAX_SKIP = 100.0              # Maximum percentage of taxes that can be skipped
BASE_MAX_PENALTY = 400.0         # Maximum penalty when caught cheating 100%

# runs the simulation with N people and R rounds
def run_simulation(N, R):
    print(f'simulation running with {N} people and {R} rounds')


def main():
    print("=== Tax Cheating Game Theory Simulation ===")
    while True:
        try:
            N = int(input("Enter the number of individuals (N): "))
            if N <= 0:
                print("Number of individuals must be positive.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for the number of individuals.")
    while True:
        try:
            R = int(input("Enter the number of rounds to simulate: "))
            if R <= 0:
                print("Number of rounds must be positive.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for the number of rounds.")
    print("\nStarting simulation...\n")
    run_simulation(N, R)


if __name__ == "__main__":
    main()
