import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import simple_simu as sim

alpha_entry, N_product_entry, P_entry, L_in_entry, N_in_entry = tk.Entry, tk.Entry, tk.Entry, tk.Entry, tk.Entry


def graph_results(flows, concentrations, title, np, **kwargs):
    stages = list(range(1, len(flows) + 1))

    fig, axes = plt.subplots(1, 2)
    fig.set_figwidth(10)
    fig.suptitle(title)
    # Plot the flow per stage
    axes[0].semilogy(stages, flows, marker='o', linestyle='-', color='b')
    axes[0].set_xlabel('Stage')
    axes[0].set_ylabel('Flow')
    axes[0].set_title('Flow(stage)')
    axes[0].grid(True)

    # Plot the concentration per stage
    axes[1].plot(stages, concentrations, marker='o', linestyle='-', color='r')
    axes[1].set_xlabel('Stage')
    axes[1].set_ylabel('Concentration')
    axes[1].set_title('N(stage)')
    axes[1].grid(True)
    axes[1].axhline(y=np, color='black', linestyle='-')

    if kwargs:
        stages_2 = list(range(1, len(kwargs["compare"]) + 1))
        axes[0].plot(stages_2, kwargs["compare"], marker='o', linestyle='-', color='g')
    plt.tight_layout()
    plt.show()


def run_simulation():
    global alpha_entry, N_product_entry, P_entry, L_in_entry, N_in_entry
    try:
        alpha = float(alpha_entry.get())
        np = float(N_product_entry.get())
        p = float(P_entry.get())
        l = float(L_in_entry.get())
        nl = float(N_in_entry.get())

        flows, concentrations = sim.calc_ideal_flows(alpha, np, p, l, nl)
        if not concentrations:
            # The parameters are not valid
            messagebox.showerror("Input Error", "Not enough U-235 in the input stream, enrichment goal can't be achieved!")
            return

        result = f"Simulated with alpha={alpha}, N_product={round(np,3)}, P={p}, L_in={l}, N_in={round(nl,2)}\n Using {len(flows)} stages"

        n_stages = sim.check_input(alpha, p, l, np, nl)
        flows_2 = sim.flow_calcs(alpha, p, np, nl, n_stages)
        graph_results(flows, concentrations, result, np, compare=flows_2)

    except SyntaxError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for all parameters.")


def add_input_field(frame, label_text, row, placeholder):
    # Function to add labels and entries
    label = ttk.Label(frame, text=label_text, background="#2e3b4e", foreground="#ffffff", font=("Helvetica", 10))
    label.grid(column=0, row=row, padx=10, pady=5, sticky='W')
    entry = ttk.Entry(frame)
    entry.insert(0, str(placeholder))
    entry.grid(column=1, row=row, padx=10, pady=5)
    return entry


def create_gui():
    global alpha_entry, N_product_entry, P_entry, L_in_entry, N_in_entry
    # Create the main window
    root = tk.Tk()
    root.title("Uranium Enrichment Cascade Simulation")
    root.geometry("500x400")
    root.configure(bg="#2e3b4e")

    # Add a title label
    title_label = tk.Label(root, text="סימולציה של קסקדות להעשרת אורניום - 235", font=("Helvetica", 16, "bold"), bg="#2e3b4e", fg="#ffffff")
    title_label.pack(pady=10)

    # Add a frame for the input fields
    input_frame = tk.Frame(root, bg="#2e3b4e")
    input_frame.pack(pady=10)

    # Create and place the labels and entry widgets
    alpha_entry = add_input_field(input_frame, "Alpha:", 0, 1.5)
    N_product_entry = add_input_field(input_frame, "N_product:", 1, 0.9)
    P_entry = add_input_field(input_frame, "P:", 2, 1)
    L_in_entry = add_input_field(input_frame, "L_in:", 3, 1000)
    N_in_entry = add_input_field(input_frame, "N_in:", 4, 1/140)

    # Add a frame for the image
    image_frame = tk.Frame(root, bg="#2e3b4e")
    image_frame.pack(pady=10)

    # Create and place the run button
    run_button = tk.Button(root, text="    Run    ", command=run_simulation, font=("Helvetica", 12), bg="#4CAF50",
                           fg="#ffffff", activebackground="#45a049", activeforeground="#ffffff")
    run_button.pack(pady=20)

    # Run the application
    root.mainloop()


if __name__ == '__main__':
    create_gui()

