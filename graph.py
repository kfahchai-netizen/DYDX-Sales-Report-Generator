from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from tkinter import Frame, Button, messagebox

def generate_graph(table):
    # Extract data from the table
    items = table.get_children()
    if not items:
        messagebox.showwarning("No Data", "No data available to generate a graph.")
        return

    # Store data
    item_codes = []
    item_names = []
    profits_deficits = []

    for item in items:
        values = table.item(item)['values']
        item_codes.append(values[0])  # Item Code
        item_names.append(values[1])  # Item Name
        profits_deficits.append(float(values[6][3:]))  # Profit/Deficit (remove "RM ")

    # Create X axis labels (Item Code / Item Name)
    x_labels = [f"{code}\n{name}" for code, name in zip(item_codes, item_names)]
    x_positions = range(len(x_labels))  # Create numeric indices for the X axis

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot the profit/deficit line 
    plt.plot(x_positions, profits_deficits, label="Profit/Deficit", color="blue", marker="o")

    # Add a black solid line at y=0
    plt.axhline(y=0, color="black", linestyle="-", linewidth=1.2)

    # Set the title and labels for the chart
    plt.title("Item Profit/Deficit", fontsize=16)
    plt.xlabel("Item Code / Item Name", fontsize=12)
    plt.ylabel("Profit/Deficit (RM)", fontsize=12)

    # Set the X axis labels
    plt.xticks(x_positions, x_labels, rotation=45, ha="right")

    # Add a legend
    plt.legend()

    # Display the grid
    plt.grid(alpha=0.3)

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()



