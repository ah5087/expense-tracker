from expense import Expense
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
        "🍳 Food", "🏡 Home", "💼 Work", "🍾 Fun", "🪴 Misc"
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


def summarize_expenses(expense_file_path, budget):
    print(f"Summarize expenses!")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(
                ",")
            line_expense = Expense(
                name=expense_name, amount=float(expense_amount), category=expense_category)
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category: ")
    for key, amount in amount_by_category.items():
        print(f" {key}: ${amount:.2f}")

    total_spent = sum([ex.amount for ex in expenses])
    print(green(f"Total Spent: ${total_spent:.2f}"))

    remaining_budget = budget - total_spent
    print(green(f"Budget Remaining: ${remaining_budget:.2f}"))

    # get current date
    now = datetime.datetime.now()

    # number of days in current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]

    # calculate number of remaining days in current month
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"Budget Per Day: ${daily_budget:.2f}"))


def green(text):
    return f"\033[92m{text}\033[0m"


def blue(text):
    return f"\033[94m{text}\033[0m"


if __name__ == "__main__":  # only true when run directly, not imported
    main()
