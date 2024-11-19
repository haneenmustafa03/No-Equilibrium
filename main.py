import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Simulation Params (Can be tweaked for increase/decrease tax cheating)
FULL_CHEAT_CAUGHT_CHANCE = 0.75    # Chance of getting caught from fully cheating
HALF_CHEAT_CAUGHT_CHANCE = 0.3     # Chance of getting caught from half cheating
FLAT_TAX = 20                       # Flat tax everyone owes
WELFARE_BASE = 40                 # Welfare pool per person (to auto scale welfare with more people)


class Individual:
    def __init__(self, id):
        self.id = id
        self.utility = 0.0
        self.x = 50.0  # how much % taxes the individual is cheating, (0, 50, or 100)
        self.times_caught = 0
        self.penalty_stack = 0
        self.probabilities = [0.0, 0.0, 0.0]  # stores last probability array for print output

    # calculates the probabilities for the mixed strategy of a player based on expected utilities
    def decide_tax_skipping(self, welfare_bonus, mechanism):
        # expected utils of strategies
        if mechanism:
            exp_ncu = welfare_bonus - FLAT_TAX
            exp_hcu = welfare_bonus - FLAT_TAX * .5 + HALF_CHEAT_CAUGHT_CHANCE * (calculate_penalty(50) + self.penalty_stack)
            exp_fcu = welfare_bonus + FULL_CHEAT_CAUGHT_CHANCE * (calculate_penalty(100) + self.penalty_stack)
        else:
            exp_ncu = welfare_bonus - FLAT_TAX
            exp_hcu = welfare_bonus - FLAT_TAX * .5
            exp_fcu = welfare_bonus

        options = [0.0, 50.0, 100.0]
        probabilities = [0.0, 0.0, 0.0]
        util_sum = 0

        smallest = abs(min(exp_ncu, exp_hcu, exp_fcu))
        exp_ncu += 1.5 * smallest
        exp_hcu += 1.5 * smallest
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
    return (-2 * x / 100.0) * FLAT_TAX


# runs the simulation with N people and R rounds
def run_simulation(N, R, mechanism, output_func=print):
    individuals = [Individual(i + 1) for i in range(N)]
    welfare = WELFARE_BASE*N
    for round_num in range(1, R + 1):
        paid_sum = 0
        output_func(f"--- Round {round_num} (Welfare: {welfare*100 / (WELFARE_BASE*N):.2f}%)---\n")
        for person in individuals:
            person.decide_tax_skipping(welfare / N, mechanism)
            x = person.x
            paid_sum += FLAT_TAX * ((100-x)/100)
            p_catch = calculate_catch_probability(x)
            caught = random.random() < p_catch
            if caught and mechanism:
                penalty = calculate_penalty(x) + person.penalty_stack
                caught_str = "Caught"
                person.times_caught += 1
                person.penalty_stack = penalty
                output_func(f"Person {person.id}: Skipped {x:.2f}% of taxes - {caught_str} - "
                           f"Penalty this round: {penalty:.2f} - Mixed Strategy: "
                           f"({person.probabilities[0] * 100:.2f}% Pay Full; "
                           f"{person.probabilities[1] * 100:.2f}% Cheat Half; "
                           f"{person.probabilities[2] * 100:.2f}% Cheat All)\n")
            else:
                utility = welfare/N - FLAT_TAX * ((100-x)/100)
                caught_str = "Not Caught"
                output_func(f"Person {person.id}: Skipped {x:.2f}% of taxes - {caught_str} - "
                           f"Utility this round: {utility:.2f} - Mixed Strategy: "
                           f"({person.probabilities[0] * 100:.2f}% Pay Full; "
                           f"{person.probabilities[1] * 100:.2f}% Cheat Half; "
                           f"{person.probabilities[2] * 100:.2f}% Cheat All)\n")
                person.utility += utility
        output_func("\n")
        welfare = (WELFARE_BASE*N) * (paid_sum / (FLAT_TAX*N))

    summary = "=== Simulation Summary ===\n"
    for person in individuals:
        summary += f"Person {person.id}: Total Utility over {R} rounds: {person.utility:.2f} - " \
                   f"Times Caught: {person.times_caught}\n"
    utilities = [person.utility for person in individuals]
    avg_utility = sum(utilities) / N
    highest_utility = max(utilities)
    lowest_utility = min(utilities)
    summary += f"\nAverage Utility: {avg_utility:.2f}\n"
    summary += f"Highest Utility: {highest_utility:.2f}\n"
    summary += f"Lowest Utility: {lowest_utility:.2f}\n"
    summary += f"Final Welfare: {welfare*100 / (WELFARE_BASE*N):.2f}%\n"
    output_func(summary)


# GUI class
class SimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tax Tragedy of the Commons Sim")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)

        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.grid(row=0, column=0, sticky=tk.W + tk.E)

        ttk.Label(top_frame, text="Number of Individuals (N):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.n_var = tk.StringVar()
        self.n_entry = ttk.Entry(top_frame, textvariable=self.n_var, width=15)
        self.n_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(top_frame, text="Number of Rounds (R):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.r_var = tk.StringVar()
        self.r_entry = ttk.Entry(top_frame, textvariable=self.r_var, width=15)
        self.r_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        self.run_button = ttk.Button(top_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=0, column=2, rowspan=2, padx=10, pady=5)

        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=30)
        self.output_text.pack(fill=tk.BOTH, expand=True)

    # puts the output at the end of the output box and scrolls to it
    def append_output(self, text):
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)

    # runs the sim and clears previous outputs
    def run_simulation(self):
        self.output_text.delete(1.0, tk.END)

        try:
            N = int(self.n_var.get())
            if N <= 0:
                raise ValueError("Number of individuals must be positive.")
        except ValueError as ve:
            messagebox.showerror("Invalid Input", f"Invalid number of individuals (N): {ve}")
            return

        try:
            R = int(self.r_var.get())
            if R <= 0:
                raise ValueError("Number of rounds must be positive.")
        except ValueError as ve:
            messagebox.showerror("Invalid Input", f"Invalid number of rounds (R): {ve}")
            return

        self.run_button.config(state=tk.DISABLED)
        run_simulation(N, R, self.append_output)
        self.run_button.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    SimGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()