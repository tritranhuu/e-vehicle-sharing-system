import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from utils.const import LARGEFONT

import utils.db_utils as db

class TopupHistoryDialog(object):
    def __init__(self, parent, uid):
        top = self.top = tk.Toplevel(parent)
        self.uid = uid
        # height = len(unpaid_rentals) * 40 + 220
        self.top.geometry(f"300x480")
        top.title("Top-up History")

        balance_label = ttk.Label(top, text="Top-up History", anchor="w", font=LARGEFONT)
        balance_label.place(x=20, y=20, width=280, height=40)

        charges_frame = ttk.LabelFrame(top, text="Your Top-up")
        charges_frame.place(x=20, y=100, width=260, height=300)

        self.charge_tree = ttk.Treeview(charges_frame)
        self.charge_tree.place(x=10, y=10, width=240, height=260)

        self.charge_tree['columns'] = ('Time', 'Amount')

        self.charge_tree.column("#0", width=0, stretch=tk.NO)
        self.charge_tree.column("Time", anchor=tk.CENTER, width=160)
        self.charge_tree.column("Amount", anchor=tk.CENTER, width=78)

        self.charge_tree.heading("Time", text="Time", anchor=tk.CENTER)
        self.charge_tree.heading("Amount", text="Amount", anchor=tk.CENTER)

        self.refresh_table()

        cancel_btn = ttk.Button(top, text='Back', command=lambda: self.top.destroy())
        cancel_btn.place(x=100, y=420, width=100, height=40)

    def refresh_table(self):
        from utils.datetime_utils import beautify_time
        top_up = db.topup_handler.get_topup_by_uid(self.uid)
        top_up.reverse()
        for data in top_up:
            value = (beautify_time(data['time']),
                     f"£{data['amount']}"
                     )
            self.charge_tree.insert(parent='', index='end', text='', values=value)






