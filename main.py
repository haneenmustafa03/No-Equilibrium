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


<<<<<<< HEAD
# calculates how likely someone is to be caught this round
def calculate_catch_probability(x, current_max_catch_prob):
    return ((x / 100) ** 2) * current_max_catch_prob


# calculates how much someone should be penalized (based on how much they cheated)
def calculate_penalty(x):
    penalty = -((x / 100) ** 2) * BASE_MAX_PENALTY
    return penalty


=======
>>>>>>> main
# runs the simulation with N people and R rounds
def run_simulation(N, R):
    individuals = [Individual(i+1) for i in range(N)]
    base_max_catch_prob = BASE_MAX_CATCH_PROB
    for round_num in range(1, R+1):
        print(f"--- Round {round_num} ---")
        average_x = sum(person.x for person in individuals) / N
        current_max_catch_prob = base_max_catch_prob * ((average_x / 100) ** 2)
        current_max_catch_prob = min(current_max_catch_prob, 1.0)
        print(f"Current Government Max Catch Probability: {current_max_catch_prob*100:.2f}% based on average tax skipped: {average_x:.2f}%")
        for person in individuals:
            person.update_scrutiny()
            person.decide_tax_skipping()
            x = person.x
            p_catch = calculate_catch_probability(x, current_max_catch_prob)
            if person.is_under_scrutiny():
                p_catch *= SCRUTINY_MULTIPLIER
                p_catch = min(p_catch, 1.0)
            caught = random.random() < p_catch
            if caught:
                penalty = calculate_penalty(x)
                utility = penalty
                caught_str = "Caught"
                person.times_caught += 1
                person.enter_scrutiny()
                print(f"Person {person.id}: Skipped {x:.2f}% of taxes - {caught_str} - Penalty this round: {penalty:.2f} - Next Round Cheating Approximate: {person.x:.2f}% - Scrutiny: Yes")
            else:
                utility = x * UTILITY_PER_PERCENT
                caught_str = "Not Caught"
                print(f"Person {person.id}: Skipped {x:.2f}% of taxes - {caught_str} - Utility this round: {utility:.2f} - Next Round Cheating Approximate: {person.x:.2f}% - Scrutiny: {'Yes' if person.is_under_scrutiny() else 'No'}")
            person.utility += utility
        print("")
    print("=== Simulation Summary ===")
    for person in individuals:
        print(f"Person {person.id}: Total Utility over {R} rounds: {person.utility:.2f} - Times Caught: {person.times_caught}")
    utilities = [person.utility for person in individuals]
    avg_utility = sum(utilities) / N
    highest_utility = max(utilities)
    lowest_utility = min(utilities)
    print(f"\nAverage Utility: {avg_utility:.2f}")
    print(f"Highest Utility: {highest_utility:.2f}")
    print(f"Lowest Utility: {lowest_utility:.2f}")


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