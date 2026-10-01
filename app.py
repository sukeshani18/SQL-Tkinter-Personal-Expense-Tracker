import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    add_expense,
    get_expenses,
    get_daily_total,
    update_expense,
    delete_expense
)


# =========================
# LOAD EXPENSES
# =========================

def load_expenses():

    # Clear table
    for item in expense_table.get_children():
        expense_table.delete(item)

    selected_date = date_entry.get().strip()

    if not selected_date:
        total_label.config(
            text="Please enter a date"
        )
        return

    expenses = get_expenses(selected_date)

    # Display expenses
    for expense in expenses:

        expense_id = expense[0]

        expense_table.insert(
            "",
            tk.END,
            iid=str(expense_id),
            values=expense[1:]
        )

    # Get updated total
    total = get_daily_total(selected_date)

    total_label.config(
        text=f"Total for {selected_date}: ₹{total:.2f}"
    )


# =========================
# ADD EXPENSE
# =========================

def add_new_expense():

    expense_date = date_entry.get().strip()
    category = category_entry.get().strip()
    description = description_entry.get().strip()
    amount = amount_entry.get().strip()

    if not expense_date or not category or not amount:

        messagebox.showwarning(
            "Missing Information",
            "Please enter Date, Category and Amount."
        )

        return

    try:
        amount = float(amount)

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid number."
        )

        return

    add_expense(
        expense_date,
        category,
        description,
        amount
    )

    load_expenses()

    category_entry.set("")

    description_entry.delete(
        0,
        tk.END
    )

    amount_entry.delete(
        0,
        tk.END
    )

    messagebox.showinfo(
        "Success",
        "Expense added successfully!"
    )


# =========================
# SELECT EXPENSE
# =========================

def fill_fields(event):

    selected_item = expense_table.selection()

    if not selected_item:
        return

    expense_id = selected_item[0]

    values = expense_table.item(
        expense_id,
        "values"
    )

    # Date
    date_entry.delete(
        0,
        tk.END
    )

    date_entry.insert(
        0,
        values[0]
    )

    # Category
    category_entry.set(
        values[1]
    )

    # Description
    description_entry.delete(
        0,
        tk.END
    )

    description_entry.insert(
        0,
        values[2]
    )

    # Amount
    amount_entry.delete(
        0,
        tk.END
    )

    amount_entry.insert(
        0,
        values[3]
    )


# =========================
# UPDATE EXPENSE
# =========================

def update_selected_expense():

    selected_item = expense_table.selection()

    if not selected_item:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense to update."
        )

        return

    expense_id = selected_item[0]

    expense_date = date_entry.get().strip()
    category = category_entry.get().strip()
    description = description_entry.get().strip()
    amount = amount_entry.get().strip()

    if not expense_date or not category or not amount:

        messagebox.showwarning(
            "Missing Information",
            "Please enter Date, Category and Amount."
        )

        return

    try:
        amount = float(amount)

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid number."
        )

        return

    update_expense(
        expense_id,
        expense_date,
        category,
        description,
        amount
    )

    load_expenses()

    messagebox.showinfo(
        "Updated",
        "Expense updated successfully!"
    )


# =========================
# DELETE EXPENSE
# =========================

def delete_selected_expense():

    selected_item = expense_table.selection()

    if not selected_item:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense to delete."
        )

        return

    expense_id = selected_item[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this expense?"
    )

    if not confirm:
        return

    try:

        deleted_rows = delete_expense(
            expense_id
        )

        if deleted_rows == 0:

            messagebox.showerror(
                "Delete Error",
                "Expense was not found in the database."
            )

            return

        # Refresh table AND total
        load_expenses()

        # Clear only category, description and amount
        category_entry.set("")

        description_entry.delete(
            0,
            tk.END
        )

        amount_entry.delete(
            0,
            tk.END
        )

        messagebox.showinfo(
            "Deleted",
            "Expense deleted successfully!"
        )

    except Exception as error:

        messagebox.showerror(
            "Database Error",
            f"Could not delete expense.\n\n{error}"
        )


# =========================
# CLEAR FORM
# =========================

def clear_form():

    date_entry.delete(
        0,
        tk.END
    )

    category_entry.set("")

    description_entry.delete(
        0,
        tk.END
    )

    amount_entry.delete(
        0,
        tk.END
    )

    total_label.config(
        text="Total for selected date: ₹0.00"
    )


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title(
    "Personal Expense Tracker"
)

root.geometry(
    "850x600"
)


# =========================
# TITLE
# =========================

title_label = tk.Label(
    root,
    text="Personal Expense Tracker",
    font=("Arial", 20, "bold")
)

title_label.pack(
    pady=15
)


# =========================
# INPUT FRAME
# =========================

input_frame = tk.Frame(root)

input_frame.pack(
    pady=10
)


# Date

tk.Label(
    input_frame,
    text="Date:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

date_entry = tk.Entry(
    input_frame,
    width=15
)

date_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


# Category

tk.Label(
    input_frame,
    text="Category:"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)

category_entry = ttk.Combobox(
    input_frame,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Other"
    ],
    width=13
)

category_entry.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)


# Description

tk.Label(
    input_frame,
    text="Description:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

description_entry = tk.Entry(
    input_frame,
    width=20
)

description_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# Amount

tk.Label(
    input_frame,
    text="Amount:"
).grid(
    row=1,
    column=2,
    padx=5,
    pady=5
)

amount_entry = tk.Entry(
    input_frame,
    width=15
)

amount_entry.grid(
    row=1,
    column=3,
    padx=5,
    pady=5
)


# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(root)

button_frame.pack(
    pady=10
)


# Add

tk.Button(
    button_frame,
    text="ADD EXPENSE",
    command=add_new_expense,
    width=15
).grid(
    row=0,
    column=0,
    padx=5
)


# Update

tk.Button(
    button_frame,
    text="UPDATE EXPENSE",
    command=update_selected_expense,
    width=15
).grid(
    row=0,
    column=1,
    padx=5
)


# Refresh

tk.Button(
    button_frame,
    text="REFRESH",
    command=load_expenses,
    width=15
).grid(
    row=0,
    column=2,
    padx=5
)


# Delete

tk.Button(
    button_frame,
    text="DELETE EXPENSE",
    command=delete_selected_expense,
    width=15
).grid(
    row=0,
    column=3,
    padx=5
)


# Clear

tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_form,
    width=15
).grid(
    row=0,
    column=4,
    padx=5
)


# =========================
# EXPENSE TABLE
# =========================

table_frame = tk.Frame(root)

table_frame.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)


columns = (
    "Date",
    "Category",
    "Description",
    "Amount"
)


expense_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


expense_table.heading(
    "Date",
    text="Date"
)

expense_table.heading(
    "Category",
    text="Category"
)

expense_table.heading(
    "Description",
    text="Description"
)

expense_table.heading(
    "Amount",
    text="Amount"
)


expense_table.column(
    "Date",
    width=100
)

expense_table.column(
    "Category",
    width=120
)

expense_table.column(
    "Description",
    width=250
)

expense_table.column(
    "Amount",
    width=120
)


expense_table.pack(
    fill="both",
    expand=True
)


# Select row

expense_table.bind(
    "<<TreeviewSelect>>",
    fill_fields
)


# =========================
# TOTAL
# =========================

total_label = tk.Label(
    root,
    text="Total for selected date: ₹0.00",
    font=("Arial", 14, "bold")
)

total_label.pack(
    pady=10
)


# =========================
# DEFAULT DATE
# =========================

date_entry.insert(
    0,
    "2026-10-01"
)


# =========================
# LOAD INITIAL DATA
# =========================

load_expenses()


# =========================
# START APPLICATION
# =========================

root.mainloop()