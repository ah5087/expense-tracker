from expense import Expense
from collections import defaultdict
import calendar
import datetime


def main():
    print(f"Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000

    # get user input of expense
    expense = get_user_expense()

    # write expense to a file
    save_expense_to_file(expense, expense_file_path)

    # read file to summarize expenses
    summarize_expenses(expense_file_path, budget)


def get_user_expense():
    print(f"Get user expense!")
    expense_name = input(blue("Enter expense name: "))
    expense_amount = float(input(blue("Enter expense amount: ")))
    expense_categories = [
        " 🍳 Food", " 🏡 Home", " 💼 Work", " 🍾 Fun", " 🪴 Misc"
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"    {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(
            input(blue(f"Enter category number {value_range}: "))) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid Category. Please try again!")


def save_expense_to_file(expense: Expense, expense_file_path):
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name}, {expense.amount}, {expense.category}\n")


def summarize_expenses(file_path, budget):
    total_expenses = 0
    expenses_by_category = defaultdict(float)

    with open(file_path, 'r') as file:
        for line in file:
            name, amount, category = line.strip().split(',')
            amount = float(amount)
            total_expenses += amount
            expenses_by_category[category] += amount

    return {
        'total_expenses': total_expenses,
        'expenses_by_category': dict(expenses_by_category)
    }


def green(text):
    return f"\033[92m{text}\033[0m"


def blue(text):
    return f"\033[94m{text}\033[0m"


if __name__ == "__main__":  # only true when run directly, not imported
    main()
