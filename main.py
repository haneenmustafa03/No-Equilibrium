import random

# Simulation Params (Can be tweaked for increase/decrease tax cheating)
UTILITY_PER_PERCENT = 1          # Utility gained per percent of tax skipped
BASE_MAX_PENALTY = 100.0         # Maximum penalty when caught cheating 100%
FULL_CHEAT_CAUGHT_CHANCE = 0.5  # Chance of getting caught from fully cheating
HALF_CHEAT_CAUGHT_CHANCE = 0.25  # Chance of getting caught from half cheating


class Individual:
    def __init__(self, id):
        self.id = id
        self.utility = 0.0
        self.x = 50.0 # how much % taxes the indidividual is cheating, (0, 50, or 100)
        self.times_caught = 0
        self.penalty_stack = 0

    def decide_tax_skipping(self):
        no_cheat_utility = 0
        half_cheat_utility = UTILITY_PER_PERCENT*50 + HALF_CHEAT_CAUGHT_CHANCE*(calculate_penalty(50)+self.penalty_stack)
        full_cheat_utility = UTILITY_PER_PERCENT*100 + FULL_CHEAT_CAUGHT_CHANCE*(calculate_penalty(100)+self.penalty_stack)

        if no_cheat_utility >= half_cheat_utility and no_cheat_utility >= full_cheat_utility:
            self.x = 0.0
        elif half_cheat_utility >= no_cheat_utility and half_cheat_utility >= full_cheat_utility:
            self.x = 50.0
        else:
            self.x = 100.0


# calculates how likely someone is to be caught this round
def calculate_catch_probability(x):
    match x:
        case 100.0:
            return FULL_CHEAT_CAUGHT_CHANCE
        case 50.0:
            return HALF_CHEAT_CAUGHT_CHANCE
        case _:
            return 0


# calculates the penalty of a tax cheat (for now its 2:1 with the amount cheated)
def calculate_penalty(x):
    return -2*x


# runs the simulation with N people and R rounds
def run_simulation(N, R):
    individuals = [Individual(i+1) for i in range(N)]
    for round_num in range(1, R+1):
        print(f"--- Round {round_num} ---")
        for person in individuals:
            person.decide_tax_skipping()
            x = person.x
            p_catch = calculate_catch_probability(x)
            caught = random.random() < p_catch
            if caught:
                penalty = calculate_penalty(x) + person.penalty_stack
                utility = penalty
                caught_str = "Caught"
                person.times_caught += 1
                person.penalty_stack = penalty
                print(f"Person {person.id}: Skipped {x:.2f}% of taxes - {caught_str} - Penalty this round: {penalty:.2f}")
            else:
                utility = x * UTILITY_PER_PERCENT
                caught_str = "Not Caught"
                print(f"Person {person.id}: Skipped {x:.2f}% of taxes - {caught_str} - Utility this round: {utility:.2f}")
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


if __name__ == "__main__":

    main()
