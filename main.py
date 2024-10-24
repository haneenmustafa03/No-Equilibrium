import random

# Simulation Params (Can be tweaked for increase/decrease tax cheating)
UTILITY_PER_PERCENT = 0.5          # Utility gained per percent of tax skipped
BASE_MAX_PENALTY = 100.0         # Maximum penalty when caught cheating 100%
FULL_CHEAT_CAUGHT_CHANCE = .75  # Chance of getting caught from fully cheating
HALF_CHEAT_CAUGHT_CHANCE = .3  # Chance of getting caught from half cheating
FLAT_TAX = 20  # Flat tax everyone owes
WELFARE_BASE = 1000  # Welfare pool


class Individual:
    def __init__(self, id):
        self.id = id
        self.utility = 0.0
        self.x = 50.0  # how much % taxes the indidividual is cheating, (0, 50, or 100)
        self.times_caught = 0
        self.penalty_stack = 0
        self.probabilities = [0.0, 0.0, 0.0]  # stores last probability array for print output

    # calculates the probabilities for the mixed strategy of a player based on expected utilities
    def decide_tax_skipping(self, welfare_bonus):
        # expected utils of strategies
        exp_ncu = welfare_bonus - FLAT_TAX
        exp_hcu = welfare_bonus - FLAT_TAX + UTILITY_PER_PERCENT*50 + HALF_CHEAT_CAUGHT_CHANCE*(calculate_penalty(50)+self.penalty_stack)
        exp_fcu = welfare_bonus - FLAT_TAX + UTILITY_PER_PERCENT*100 + FULL_CHEAT_CAUGHT_CHANCE*(calculate_penalty(100)+self.penalty_stack)

        options = [0.0, 50.0, 100.0]
        probabilities = [0.0, 0.0, 0.0]
        util_sum = 0
        """if exp_ncu >= 0 and exp_hcu >= 0 and exp_fcu >= 0:  # all positive
            util_sum += exp_ncu + exp_hcu + exp_fcu
            probabilities[0] = exp_ncu/util_sum
            probabilities[1] = exp_hcu/util_sum
            probabilities[2] = exp_fcu/util_sum
        elif exp_ncu <= 0 and exp_hcu <= 0 and exp_fcu <= 0:  # all negative
            util_sum += exp_ncu + exp_hcu + exp_fcu
            probabilities[0] = 1.0 - (exp_ncu / util_sum)
            probabilities[1] = 1.0 - (exp_hcu / util_sum)
            probabilities[2] = 1.0 - (exp_fcu / util_sum)
            prob_sum = sum(probabilities)
            probabilities[0] = probabilities[0]/prob_sum
            probabilities[1] = probabilities[1]/prob_sum
            probabilities[2] = probabilities[2]/prob_sum
        else:  # some negative, some positive"""
        smallest = abs(min(exp_ncu, exp_hcu, exp_fcu))
        if exp_ncu > exp_hcu and exp_ncu > exp_fcu:
            exp_ncu = (exp_ncu + 1.5 * smallest) * 2
        else:
            exp_ncu += 1.5 * smallest
        if exp_hcu > exp_ncu and exp_hcu > exp_fcu:
            exp_hcu = (exp_hcu + 1.5 * smallest) * 2
        else:
            exp_hcu += 1.5 * smallest
        if exp_fcu > exp_hcu and exp_fcu > exp_ncu:
            exp_fcu = (exp_fcu + 1.5 * smallest) * 2
        else:
            exp_fcu += 1.5 * smallest
        util_sum += exp_ncu + exp_hcu + exp_fcu
        probabilities[0] = exp_ncu / util_sum
        probabilities[1] = exp_hcu / util_sum
        probabilities[2] = exp_fcu / util_sum
        self.probabilities = probabilities
        self.x = random.choices(options, weights=probabilities, k=1)[0]


# calculates how likely someone is to be caught this round
def calculate_catch_probability(x):
    match x:
        case 100.0:
            return FULL_CHEAT_CAUGHT_CHANCE
        case 50.0:
            return HALF_CHEAT_CAUGHT_CHANCE
        case _:
            return 0


# calculates the penalty of a tax cheat
def calculate_penalty(x):
    return (-2*x/100.0) * FLAT_TAX


# runs the simulation with N people and R rounds
def run_simulation(N, R):
    individuals = [Individual(i+1) for i in range(N)]
    welfare = WELFARE_BASE
    for round_num in range(1, R+1):
        paid_sum = 0
        print(f"--- Round {round_num} (Welfare: {welfare*100/WELFARE_BASE:.2f}%)---")
        for person in individuals:
            person.decide_tax_skipping(welfare/N)
            x = person.x
            paid_sum += 100-x
            p_catch = calculate_catch_probability(x)
            caught = random.random() < p_catch
            if caught:
                penalty = calculate_penalty(x) + person.penalty_stack
                utility = penalty
                caught_str = "Caught"
                person.times_caught += 1
                person.penalty_stack = penalty
                print(f"Person {person.id}: Skipped {x:.2f}% of taxes - {caught_str} - Penalty this round: {penalty:.2f} - Mixed Strategy: ({person.probabilities[0]*100:.2f}% Pay Full; {person.probabilities[1]*100:.2f}% Cheat Half; {person.probabilities[2]*100:.2f}% Cheat All)")
            else:
                utility = x * UTILITY_PER_PERCENT
                caught_str = "Not Caught"
                print(f"Person {person.id}: Skipped {x:.2f}% of taxes - {caught_str} - Utility this round: {utility:.2f} - Mixed Strategy: ({person.probabilities[0]*100:.2f}% Pay Full; {person.probabilities[1]*100:.2f}% Cheat Half; {person.probabilities[2]*100:.2f}% Cheat All)")
            person.utility += utility
        print("")
        welfare = WELFARE_BASE * (paid_sum/(N*100))

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

