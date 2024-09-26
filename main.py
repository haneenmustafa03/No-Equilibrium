import random

# Simulation Params (Can be tweaked for increase/decrease tax cheating)
BASE_MAX_CATCH_PROB = 0.5        # Base maximum probability of catching an individual
UTILITY_PER_PERCENT = 1          # Utility gained per percent of tax skipped
LEARNING_RATE_IF_CAUGHT = 0.2    # Learning rate adjustment if caught
LEARNING_RATE_IF_NOT_CAUGHT = 0.05
SCRUTINY_MULTIPLIER = 3.0        # Multiplier for catch probability during scrutiny
SCRUTINY_DURATION = 4            # Number of rounds an individual is under scrutiny
MAX_TAX_SKIP = 100.0              # Maximum percentage of taxes that can be skipped
BASE_MAX_PENALTY = 400.0         # Maximum penalty when caught cheating 100%


class Individual:
    def __init__(self, id):
        self.id = id
        self.x = random.uniform(30.0, 50.0)  # First Round Tax Skip Percent
        self.utility = 0.0
        self.times_caught = 0
        self.scrutiny_rounds_left = 0

    def decide_tax_skipping(self):
        variation = random.uniform(-5, 5)
        new_x = self.x + variation
        self.x = max(0.0, min(MAX_TAX_SKIP, new_x))

    def update_strategy(self, caught):
        if caught:
            self.x -= LEARNING_RATE_IF_CAUGHT * self.x
            self.x = max(0.0, self.x)
        else:
            self.x += LEARNING_RATE_IF_NOT_CAUGHT * (MAX_TAX_SKIP - self.x)
            self.x = min(MAX_TAX_SKIP, self.x)

    def enter_scrutiny(self):
        self.scrutiny_rounds_left = SCRUTINY_DURATION

    def update_scrutiny(self):
        if self.scrutiny_rounds_left > 0:
            self.scrutiny_rounds_left -= 1

    def is_under_scrutiny(self):
        return self.scrutiny_rounds_left > 0


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
