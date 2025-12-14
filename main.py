import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bank.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    acc_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    pin TEXT,
    balance REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acc_no INTEGER,
    message TEXT,
    date TEXT
)
""")
conn.commit()

current_acc = None

# ---------------- CREATE ACCOUNT ----------------
def create_account():
    name = simpledialog.askstring("Create Account", "Enter Name")
    pin = simpledialog.askstring("Create Account", "Set 4-digit PIN", show="*")

    if not name or not pin:
        return

    if len(pin) != 4 or not pin.isdigit():
        messagebox.showerror("Error", "PIN must be 4 digits")
        return

    cur.execute("INSERT INTO accounts (name, pin, balance) VALUES (?, ?, ?)",
                (name, pin, 0))
    conn.commit()

    acc_no = cur.lastrowid
    messagebox.showinfo("Success", f"Account Created!\nAccount No: {acc_no}")

# ---------------- LOGIN ----------------
def login():
    global current_acc
    acc = simpledialog.askinteger("Login", "Enter Account Number")
    pin = simpledialog.askstring("Login", "Enter PIN", show="*")

    cur.execute("SELECT * FROM accounts WHERE acc_no=? AND pin=?", (acc, pin))
    user = cur.fetchone()

    if user:
        current_acc = acc
        messagebox.showinfo("Login Successful", f"Welcome {user[1]}")
        user_dashboard()
    else:
        messagebox.showerror("Error", "Invalid Account Number or PIN")

# ---------------- USER FUNCTIONS ----------------
def deposit():
    amount = simpledialog.askfloat("Deposit", "Enter Amount")
    if amount and amount > 0:
        cur.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no=?",
                    (amount, current_acc))
        cur.execute("INSERT INTO transactions VALUES (NULL, ?, ?, ?)",
                    (current_acc, f"Deposited ₹{amount}", datetime.now()))
        conn.commit()
        messagebox.showinfo("Success", "Deposit Successful")

def withdraw():
    amount = simpledialog.askfloat("Withdraw", "Enter Amount")
    cur.execute("SELECT balance FROM accounts WHERE acc_no=?", (current_acc,))
    bal = cur.fetchone()[0]

    if amount and amount > 0:
        if amount > bal:
            messagebox.showerror("Error", "Insufficient Balance")
            return
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE acc_no=?",
                    (amount, current_acc))
        cur.execute("INSERT INTO transactions VALUES (NULL, ?, ?, ?)",
                    (current_acc, f"Withdrawn ₹{amount}", datetime.now()))
        conn.commit()
        messagebox.showinfo("Success", "Withdrawal Successful")

def check_balance():
    cur.execute("SELECT balance FROM accounts WHERE acc_no=?", (current_acc,))
    bal = cur.fetchone()[0]
    messagebox.showinfo("Balance", f"Current Balance: ₹{bal}")

def transaction_history():
    cur.execute("SELECT message FROM transactions WHERE acc_no=?", (current_acc,))
    rows = cur.fetchall()
    if not rows:
        messagebox.showinfo("History", "No transactions yet")
    else:
        messagebox.showinfo("History", "\n".join(r[0] for r in rows))

def mini_statement():
    cur.execute("""
    SELECT message FROM transactions
    WHERE acc_no=?
    ORDER BY id DESC LIMIT 5
    """, (current_acc,))
    rows = cur.fetchall()
    if not rows:
        messagebox.showinfo("Mini Statement", "No transactions yet")
    else:
        messagebox.showinfo("Mini Statement", "\n".join(r[0] for r in rows))

def add_interest():
    cur.execute("SELECT balance FROM accounts WHERE acc_no=?", (current_acc,))
    bal = cur.fetchone()[0]
    interest = bal * 0.05

    cur.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no=?",
                (interest, current_acc))
    cur.execute("INSERT INTO transactions VALUES (NULL, ?, ?, ?)",
                (current_acc, f"Interest Added ₹{round(interest,2)}", datetime.now()))
    conn.commit()

    messagebox.showinfo("Interest", f"Interest Added ₹{round(interest,2)}")

def loan():
    amount = simpledialog.askfloat("Loan", "Enter Loan Amount")
    if amount and amount > 0:
        cur.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no=?",
                    (amount, current_acc))
        cur.execute("INSERT INTO transactions VALUES (NULL, ?, ?, ?)",
                    (current_acc, f"Loan Taken ₹{amount}", datetime.now()))
        conn.commit()
        messagebox.showinfo("Loan", "Loan Approved")

def logout(win):
    global current_acc
    current_acc = None
    win.destroy()

# ---------------- USER DASHBOARD ----------------
def user_dashboard():
    win = tk.Toplevel(root)
    win.title("User Dashboard")
    win.geometry("320x420")

    tk.Label(win, text="Banking Menu", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Button(win, text="Deposit", width=25, command=deposit).pack(pady=5)
    tk.Button(win, text="Withdraw", width=25, command=withdraw).pack(pady=5)
    tk.Button(win, text="Check Balance", width=25, command=check_balance).pack(pady=5)
    tk.Button(win, text="Transaction History", width=25, command=transaction_history).pack(pady=5)
    tk.Button(win, text="Mini Statement", width=25, command=mini_statement).pack(pady=5)
    tk.Button(win, text="Add Interest", width=25, command=add_interest).pack(pady=5)
    tk.Button(win, text="Apply Loan", width=25, command=loan).pack(pady=5)
    tk.Button(win, text="Logout", width=25, command=lambda: logout(win)).pack(pady=10)

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Banking System")
root.geometry("300x260")

tk.Label(root, text="BANKING SYSTEM", font=("Arial", 16, "bold")).pack(pady=20)

tk.Button(root, text="Create Account", width=20, command=create_account).pack(pady=5)
tk.Button(root, text="Login", width=20, command=login).pack(pady=5)
tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=10)

root.mainloop()