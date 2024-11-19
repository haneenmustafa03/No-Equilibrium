import random
import tkinter as tk
from tkinter import scrolledtext
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import threading

# Simulation Params (Can be tweaked for increase/decrease tax cheating)
FULL_CHEAT_CAUGHT_CHANCE = 0.75  # Chance of getting caught from fully cheating
HALF_CHEAT_CAUGHT_CHANCE = 0.3  # Chance of getting caught from half cheating
FLAT_TAX = 20  # Flat tax everyone owes
WELFARE_BASE = 40  # Welfare pool per person (to auto scale welfare with more people)


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
def run_simulation_main(N, R, mechanism, output_func=print, progress_callback=None):
    individuals = [Individual(i + 1) for i in range(N)]
    welfare = WELFARE_BASE * N
    for round_num in range(1, R + 1):
        paid_sum = 0
        output_func(f"--- Round {round_num} (Welfare: {welfare * 100 / (WELFARE_BASE * N):.2f}%)---\n")
        for person in individuals:
            person.decide_tax_skipping(welfare / N, mechanism)
            x = person.x
            paid_sum += FLAT_TAX * ((100 - x) / 100)
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
                utility = welfare / N - FLAT_TAX * ((100 - x) / 100)
                caught_str = "Not Caught"
                output_func(f"Person {person.id}: Skipped {x:.2f}% of taxes - {caught_str} - "
                           f"Utility this round: {utility:.2f} - Mixed Strategy: "
                           f"({person.probabilities[0] * 100:.2f}% Pay Full; "
                           f"{person.probabilities[1] * 100:.2f}% Cheat Half; "
                           f"{person.probabilities[2] * 100:.2f}% Cheat All)\n")
                person.utility += utility
        output_func("\n")
        welfare = (WELFARE_BASE * N) * (paid_sum / (FLAT_TAX * N))

        if progress_callback:
            progress_callback(round_num, R)

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
    summary += f"Final Welfare: {welfare * 100 / (WELFARE_BASE * N):.2f}%\n"
    output_func(summary)


# GUI class
class SimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tax Tragedy of the Commons Simulation")
        self.root.geometry("1150x800")

        self.style = Style(theme='superhero')

        main_frame = tb.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        input_frame = tb.LabelFrame(main_frame, text="Simulation Parameters", padding=15)
        input_frame.pack(fill=X, pady=10)

        tb.Label(input_frame, text="Number of Individuals (N):").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.n_var = tk.IntVar(value=100)
        self.n_spinbox = tb.Spinbox(input_frame, from_=1, to=1000, textvariable=self.n_var, width=10)
        self.n_spinbox.grid(row=0, column=1, sticky=W, padx=5, pady=5)

        tb.Label(input_frame, text="Number of Rounds (R):").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.r_var = tk.IntVar(value=100)
        self.r_spinbox = tb.Spinbox(input_frame, from_=1, to=1000, textvariable=self.r_var, width=10)
        self.r_spinbox.grid(row=1, column=1, sticky=W, padx=5, pady=5)

        buttons_frame = tb.Frame(main_frame, padding=10)
        buttons_frame.pack(fill=X, pady=10)

        self.run_button = tb.Button(buttons_frame, text="Run Simulation", bootstyle=SUCCESS, command=self.run_simulation_thread)
        self.run_button.pack(side=LEFT, padx=10)

        self.run_no_mech_button = tb.Button(buttons_frame, text="Run Simulation without Mechanism", bootstyle=WARNING, command=self.run_simulation_no_mechanism_thread)
        self.run_no_mech_button.pack(side=LEFT, padx=10)

        self.progress = tb.Progressbar(main_frame, orient=HORIZONTAL, mode='determinate')
        self.progress.pack(fill=X, pady=10)

        output_frame = tb.LabelFrame(main_frame, text="Simulation Output", padding=10)
        output_frame.pack(fill=BOTH, expand=True, pady=10)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=20, font=("Consolas", 10))
        self.output_text.pack(fill=BOTH, expand=True)

    # Append to textbox (works with threading)
    def append_output(self, text):
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)

    # Update progress bar
    def update_progress(self, current, total):
        progress_percentage = (current / total) * 100
        self.progress['value'] = progress_percentage
        self.root.update_idletasks()

    # Disable buttons
    def disable_buttons(self):
        self.run_button.config(state=DISABLED)
        self.run_no_mech_button.config(state=DISABLED)

    # Enable buttons
    def enable_buttons(self):
        self.run_button.config(state=NORMAL)
        self.run_no_mech_button.config(state=NORMAL)

    # Clear output
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    # Run sim in a thread
    def run_simulation_thread(self):
        self.clear_output()
        self.disable_buttons()
        N = int(self.n_var.get())
        R = int(self.r_var.get())
        simulation_thread = threading.Thread(target=self.run_simulation, args=(N, R, True))
        simulation_thread.start()

    # Run sim in a thread (with no mechanism)
    def run_simulation_no_mechanism_thread(self):
        self.clear_output()
        self.disable_buttons()
        N = self.n_var.get()
        R = self.r_var.get()
        simulation_thread = threading.Thread(target=self.run_simulation, args=(N, R, False))
        simulation_thread.start()

    def run_simulation(self, N, R, mechanism):
        run_simulation_main(N, R, mechanism, self.append_output, self.update_progress)
        self.enable_buttons()

def main():
    root = tb.Window()
    SimGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
