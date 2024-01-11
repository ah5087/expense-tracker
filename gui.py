import tkinter as tk
from expense_tracker import save_expense_to_file, summarize_expenses
from expense import Expense


def add_expense():
    try:
        name = name_var.get()
        name_var.set("")  # Clear the field after getting the value
        amount = float(amount_var.get())
        amount_var.set("")  # Clear the field after getting the value
        category = category_var.get()
        expense = Expense(name, category, amount)
        save_expense_to_file(expense, "expenses.csv")
        update_summary()
    except ValueError:
        print(red("Invalid input. Please try again!"))


def update_budget():
    try:
        global budget
        budget = float(budget_entry.get())
        update_summary()
    except ValueError:
        print(red("Please enter a valid number for the budget!"))


def update_summary():
    summary_data = summarize_expenses("expenses.csv", budget)
    total_expenses = summary_data['total_expenses']
    expenses_by_category = summary_data['expenses_by_category']

    total_expenses_label.config(text=f"Total Expenses: ${total_expenses:.2f}")
    remaining_budget_label.config(
        text=f"Remaining Budget: ${budget - total_expenses:.2f}")

    # initialize all category labels to zero
    for category_label in category_labels.values():
        category_label.config(
            text=f"{category_label.cget('text').split(':')[0]}: $0.00")

    # update the label for each category
    for category, amount in expenses_by_category.items():
        if category in category_labels:
            category_labels[category].config(text=f"{category}: ${amount:.2f}")
        else:
            print(f"Warning: Category '{category}' in file but not in GUI")


def placeholder_focus_out(event, entry, text):
    if not entry.get():
        entry.insert(0, text)


def placeholder_focus_in(event, entry, text):
    if entry.get() == text:
        entry.delete(0, tk.END)


def red(text):
    return f"\033[91m{text}\033[0m"


budget = 500

root = tk.Tk()
root.title("Expense Tracker")

# placeholder text setup
name_var = tk.StringVar()
amount_var = tk.StringVar()

# create widgets
name_entry = tk.Entry(root, textvariable=name_var)
name_entry.insert(0, "Item Name")
name_entry.bind("<FocusIn>", lambda event: placeholder_focus_in(
    event, name_entry, "Item Name"))
name_entry.bind("<FocusOut>", lambda event: placeholder_focus_out(
    event, name_entry, "Item Name"))

amount_entry = tk.Entry(root, textvariable=amount_var)
amount_entry.insert(0, "Cost")
amount_entry.bind("<FocusIn>", lambda event: placeholder_focus_in(
    event, amount_entry, "Cost"))
amount_entry.bind("<FocusOut>", lambda event: placeholder_focus_out(
    event, amount_entry, "Cost"))

category_var = tk.StringVar(root)
category_var.set("🍳 Food")  # default value
category_menu = tk.OptionMenu(
    root, category_var, "🍳 Food", "🏡 Home", "💼 Work", "🍾 Fun", "🪴 Misc")
submit_button = tk.Button(root, text="Add Expense", command=add_expense)
budget_entry = tk.Entry(root)  # entry for budget
budget_entry.insert(0, str(budget))  # set initial budget
update_budget_button = tk.Button(
    root, text="Update Budget", command=update_budget)

# summary Labels
total_expenses_label = tk.Label(root, text="Total Expenses: $0")
remaining_budget_label = tk.Label(root, text=f"Remaining Budget: ${budget}")

# layout widgets
name_entry.pack()
amount_entry.pack()
category_menu.pack()
submit_button.pack()
tk.Label(root, text="Budget:").pack()
budget_entry.pack()
update_budget_button.pack()
total_expenses_label.pack()
remaining_budget_label.pack()

# category expenses labels
category_expenses_frame = tk.Frame(root)
category_expenses_frame.pack()
category_labels = {}
# Ensure these match exactly with your CSV
categories = [" 🍳 Food", " 🏡 Home", " 💼 Work", " 🍾 Fun", " 🪴 Misc"]
for category in categories:
    label = tk.Label(category_expenses_frame, text=f"{category}: $0.00")
    label.pack()
    category_labels[category] = label


root.mainloop()
