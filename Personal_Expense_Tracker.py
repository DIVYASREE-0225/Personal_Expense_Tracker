import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict

FILENAME = "expenses.csv"

# Create file with header if not exists
if not os.path.exists(FILENAME):
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Note"])

def center_messagebox():
    root.eval('tk::PlaceWindow . center')

def add_expense():
    date = entry_date.get()
    category = entry_category.get()
    amount = entry_amount.get()
    note = entry_note.get()

    if not (date and category and amount):
        center_messagebox()
        messagebox.showerror("Error", "Please fill in all fields except note.")
        return

    try:
        amount = float(amount)
    except ValueError:
        center_messagebox()
        messagebox.showerror("Error", "Amount must be a number.")
        return

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, note])

    center_messagebox()
    messagebox.showinfo("Success", "Expense added successfully!")
    clear_fields()
    load_expenses()

def clear_fields():
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_note.delete(0, tk.END)

def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    total = 0.0
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row)
            total += float(row[2])
    label_total.config(text=f"Total Expense: ₹{total:.2f}")

def clear_expenses():
    answer = messagebox.askyesno("Confirm", "Are you sure you want to delete all expenses?")
    if answer:
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Note"])
        load_expenses()
        center_messagebox()
        messagebox.showinfo("Cleared", "All expenses have been deleted.")

def show_pie_chart():
    category_totals = defaultdict(float)

    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            category = row[1]
            try:
                amount = float(row[2])
                category_totals[category] += amount
            except ValueError:
                continue

    if not category_totals:
        center_messagebox()
        messagebox.showinfo("No Data", "No expenses available for pie chart.")
        return

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title("Expense Distribution by Category")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def show_monthly_report():
    month = simpledialog.askstring("Monthly Report", "Enter month (YYYY-MM):")
    if not month:
        return

    total = 0.0
    expenses_in_month = []

    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0].startswith(month):
                expenses_in_month.append(row)
                try:
                    total += float(row[2])
                except ValueError:
                    continue

    if not expenses_in_month:
        center_messagebox()
        messagebox.showinfo("No Data", f"No expenses found for {month}.")
    else:
        report = f"Expenses for {month}:\n\n"
        for row in expenses_in_month:
            report += f"Date: {row[0]}, Category: {row[1]}, Amount: ₹{row[2]}, Note: {row[3]}\n"
        report += f"\nTotal for {month}: ₹{total:.2f}"

        center_messagebox()
        messagebox.showinfo(f"Monthly Report - {month}", report)

def delete_selected_expense():
    selected_item = tree.selection()
    if not selected_item:
        center_messagebox()
        messagebox.showwarning("No Selection", "Please select an expense to delete.")
        return

    answer = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected expense?")
    if not answer:
        return

    selected_values = tree.item(selected_item, 'values')

    expenses = []
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            expenses.append(row)

    for i, row in enumerate(expenses):
        if tuple(row) == selected_values:
            del expenses[i]
            break

    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(expenses)

    load_expenses()
    center_messagebox()
    messagebox.showinfo("Deleted", "Expense deleted successfully.")

# GUI Window
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("640x500")
root.config(bg="#ffcea8")

# Entry Fields
tk.Label(root, text="Date (YYYY-MM-DD)", bg="#ffcea8", fg="black").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_date = tk.Entry(root)
entry_date.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Category", bg="#ffcea8", fg="black").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_category = tk.Entry(root)
entry_category.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Amount", bg="#ffcea8", fg="black").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_amount = tk.Entry(root)
entry_amount.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Note", bg="#ffcea8", fg="black").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_note = tk.Entry(root)
entry_note.grid(row=3, column=1, padx=10, pady=5)

# Buttons (Top Row)
tk.Button(root, text="Add Expense", command=add_expense, bg="#da72b2", fg="white", width=20).grid(row=4, column=0, pady=5)
tk.Button(root, text="Show Pie Chart", command=show_pie_chart, bg="#3498db", fg="white", width=20).grid(row=4, column=1, pady=5)
tk.Button(root, text="Monthly Report", command=show_monthly_report, bg="#f1c40f", fg="black", width=20).grid(row=4, column=2, pady=5)
tk.Button(root, text="Delete Selected Expense", command=delete_selected_expense, bg="#c0392b", fg="white", width=20).grid(row=4, column=3, pady=5)

# Treeview Table
columns = ("Date", "Category", "Amount", "Note")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

# Total Label
label_total = tk.Label(root, text="Total Expense: ₹0.00", font=("Arial", 12, "bold"), bg="#ffcea8", fg="purple")
label_total.grid(row=6, column=0, columnspan=5, pady=10)

# Clear Expenses Button (Moved Below Total)
tk.Button(root, text="Clear All Expenses", command=clear_expenses, bg="#e74c3c", fg="white", width=30).grid(row=7, column=0, columnspan=5, pady=10)

load_expenses()
root.mainloop()
