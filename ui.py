import tkinter as tk
from tkinter import ttk
import pandas as pd
from planner import calculate_requirements

class EventPlannerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Event Planner")

        # Load datasets
        self.event_planning_df = pd.read_csv("Cases.csv")
        self.food_item_df = pd.read_csv("Food_db.csv")
        self.instruction_df = pd.read_csv("Instructions.csv")

        # Create labels and entry fields
        self.create_widgets()

    def create_widgets(self):
        # Create labels
        tk.Label(self.master, text="Event Type:").grid(row=0, column=0, sticky="w")
        tk.Label(self.master, text="Food Type:").grid(row=1, column=0, sticky="w")
        tk.Label(self.master, text="Number of People:").grid(row=2, column=0, sticky="w")
        tk.Label(self.master, text="Number of Food Items:").grid(row=3, column=0, sticky="w")
        tk.Label(self.master, text="Number of Drink Items:").grid(row=4, column=0, sticky="w")
        tk.Label(self.master, text="Additional Items (comma-separated):").grid(row=5, column=0, sticky="w")

        # Create entry fields
        self.event_type_entry = tk.Entry(self.master)
        self.event_type_entry.grid(row=0, column=1)
        self.food_type_entry = tk.Entry(self.master)
        self.food_type_entry.grid(row=1, column=1)
        self.num_people_entry = tk.Entry(self.master)
        self.num_people_entry.grid(row=2, column=1)
        self.num_food_items_entry = tk.Entry(self.master)
        self.num_food_items_entry.grid(row=3, column=1)
        self.num_drink_items_entry = tk.Entry(self.master)
        self.num_drink_items_entry.grid(row=4, column=1)
        self.additional_items_entry = tk.Entry(self.master)
        self.additional_items_entry.grid(row=5, column=1)

        # Create calculate button
        tk.Button(self.master, text="Calculate", command=self.calculate_event).grid(row=6, column=0, columnspan=2)

    def calculate_event(self):
        # Get input values from entry fields
        event_type = self.event_type_entry.get()
        food_type = self.food_type_entry.get()
        num_people = int(self.num_people_entry.get())
        num_food_items = int(self.num_food_items_entry.get())
        num_drink_items = int(self.num_drink_items_entry.get())
        additional_items = self.additional_items_entry.get().split() if self.additional_items_entry.get() else None

        # Calculate requirements
        num_workers, suggested_food_items, suggested_drink_items, required_items, required_utensils, instructions = calculate_requirements(event_type, food_type, num_people, num_food_items, num_drink_items, additional_items)

        # Display results
        self.display_result("Number of workers required:", str(num_workers), 7)
        self.display_result("Suggested food items:", ", ".join(suggested_food_items), 8)
        self.display_result("Suggested drink items:", ", ".join(suggested_drink_items), 9)
        self.display_result("Required items:", required_items.to_string(), 10)
        self.display_result("Required utensils:", required_utensils.to_string(), 11)
        self.display_result("Instructions:", instructions, 12)

    def display_result(self, label_text, result_text, row):
        # Create a label for the result and place it in the first column
        label = tk.Label(self.master, text=label_text)
        label.grid(row=row, column=0, sticky="w")

        # Create a text box for displaying the result and place it in the second column
        result_box = tk.Text(self.master, height=5, width=50)
        result_box.grid(row=row, column=1)

        # Insert the result text into the text box
        result_box.insert(tk.END, result_text)


def main():
    root = tk.Tk()
    app = EventPlannerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
