import tkinter as tk
from tkinter import ttk, messagebox
import re
import datetime
import utils.db_utils as db

class TopupDialog(object):
    def __init__(self, parent, uid):
        self.uid = uid
        top = self.top = tk.Toplevel(parent)

        self.top.geometry(f"600x250")
        top.title("Top-up")

        amount_label = ttk.Label(top, text="Top-up amount", anchor="w")
        amount_label.place(x=20, y=20, width=120, height=30)
        self.amount_entry = ttk.Entry(top)
        self.amount_entry.place(x=150, y=20, width=200, height=30)

        payment_frame = ttk.LabelFrame(top, text="Payment Information")
        payment_frame.place(x=20, y=60, width=560, height=130)

        account_num_label = ttk.Label(payment_frame, text="Account Number")
        account_name_label = ttk.Label(payment_frame, text="Account Name")
        expire_label = ttk.Label(payment_frame, text="Expire Date")
        cvv_label = ttk.Label(payment_frame, text="CVV")

        account_num_label.place(x=10, y=10, width=150, height=30)
        account_name_label.place(x=10, y=60, width=150, height=30)
        expire_label.place(x=400, y=10, width=80, height=30)
        cvv_label.place(x=400, y=60, width=80, height=30)

        self.account_num_entry = ttk.Entry(payment_frame)
        self.account_name_entry = ttk.Entry(payment_frame)
        self.expire_entry = ttk.Entry(payment_frame)
        self.cvv_entry = ttk.Entry(payment_frame)

        self.account_num_entry.place(x=170, y=10, width=200, height=30)
        self.account_name_entry.place(x=170, y=60, width=200, height=30)
        self.expire_entry.place(x=480, y=10, width=70, height=30)
        self.cvv_entry.place(x=480, y=60, width=70, height=30)

        confirm_btn = ttk.Button(top, text="Confirm", command=self.on_click_confirm)
        confirm_btn.place(x=360, y=200, width=100, height=40)

        cancel_btn = ttk.Button(top, text="Cancel", command=lambda: self.top.destroy())
        cancel_btn.place(x=480, y=200, width=100, height=40)

    def is_information_valid(self):
        # Check Top-up amount
        topup_amount = self.amount_entry.get()
        if not re.match(r'^\d+(\.\d+)?$', topup_amount):
            messagebox.showerror("Error", "Top-up amount should be a number")
            return False
        try:
            topup_amount = float(topup_amount)
        except:
            messagebox.showerror("Error", "Invalid amount")
            return False
        # Check Account Number
        account_num = self.account_num_entry.get()
        if not re.match(r'^\d{16}$', account_num):
            messagebox.showerror("Error", "Account Number should be a 16 digit number")
            return False

        # Check Account Name
        account_name = self.account_name_entry.get()
        if not re.match(r'^[A-Za-z ]+$', account_name):
            messagebox.showerror("Error", "Account Name can only contain English letters and spaces")
            return False

        # Check Expire Date
        expire_date = self.expire_entry.get()
        if not re.match(r'^(0[1-9]|1[0-2])\/(2[3-9]|[3-9]\d)$', expire_date):
            messagebox.showerror("Error", "Expire Date is invalid")
            return False

        # Check if Expire Date is before "11/23"
        expire_month, expire_year = map(int, expire_date.split('/'))
        current_date = datetime.datetime.now()
        if expire_year < current_date.year - 2000 or (expire_year == current_date.year - 2000 and expire_month < current_date.month):
            messagebox.showerror("Error", "Your card has expired")
            return False

        # Check CVV
        cvv = self.cvv_entry.get()
        if not re.match(r'^\d{3}$', cvv):
            messagebox.showerror("Error", "CVV should be a 3-digit number")
            return False

        return True

    def on_click_confirm(self):
        user = db.user_handler.get_user_info_by_id(self.uid)
        if self.is_information_valid():
            amount = float(self.amount_entry.get())
            db.topup_handler.create_topup(self.uid, amount)
            db.user_handler.update_user_by_id(self.uid, fields={'balance': user['balance'] + amount})
            self.top.destroy()
