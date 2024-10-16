import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import utils.db_utils as db
from entities.rental import Rental


class PayDialog(object):
    def __init__(self, parent):
        self.uid = parent.uid
        user = db.user_handler.get_user_info_by_id(self.uid)
        top = self.top = tk.Toplevel(parent)
        top.title("Pay")

        self.top.geometry(f"500x700")

        # Header
        self.balance_label = ttk.Label(top, text=f"Current Balance: £{user['balance']}", anchor="w",
                                       font=('MonoLisa', 15))
        self.balance_label.place(x=20, y=20, width=300, height=50)

        topup_btn = ttk.Button(top, text="Top up", command=self.on_click_topup)
        topup_btn.place(x=390, y=20, width=100, height=30)
        history_btn = ttk.Button(top, text="Top up History", command=self.on_click_topup_history)
        history_btn.place(x=390, y=60, width=100, height=30)

        # Body (bills, pay button)
        charges_frame = ttk.LabelFrame(top, text="Below are your remaining charges")
        charges_frame.place(x=30, y=100, width=440, height=500)

        self.charge_tree = ttk.Treeview(charges_frame)
        self.charge_tree.place(x=10, y=10, width=420, height=200)

        self.charge_tree['columns'] = ('ID', "From-To", "Duration", "Charge", "Status")

        self.charge_tree.column("#0", width=0, stretch=tk.NO)
        self.charge_tree.column("ID", anchor=tk.CENTER, width=30)
        self.charge_tree.column("From-To", anchor=tk.CENTER, width=200)
        self.charge_tree.column("Duration", anchor=tk.CENTER, width=80)
        self.charge_tree.column("Charge", anchor=tk.CENTER, width=60)
        self.charge_tree.column("Status", anchor=tk.CENTER, width=48)

        self.charge_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.charge_tree.heading("From-To", text="From-To", anchor=tk.CENTER)
        self.charge_tree.heading("Duration", text="Duration", anchor=tk.CENTER)
        self.charge_tree.heading("Charge", text="Charge", anchor=tk.CENTER)
        self.charge_tree.heading("Status", text="Status", anchor=tk.CENTER)

        self.charge_detail = tk.Message(charges_frame, width=400)
        self.charge_detail.configure(font=('MonoLisa', 10, 'bold'), bg='#eaf4fa', fg='#187dc8')
        self.charge_detail.place(x=10, y=220, width=420, height=200)

        self.total_message = tk.Message(charges_frame, width=400, anchor='e')
        self.total_message.place(x=12, y=180, width=416, height=28)
        self.total_message.configure(font=("Arial", 9, 'bold'), bg='white')

        self.refresh_table()

        self.show_btn = ttk.Button(charges_frame, text="Show All", command=lambda: self.on_click_show(True))
        self.show_btn.place(x=20, y=440, width=100, height=30)
        pay_all_btn = ttk.Button(charges_frame, text="Pay All", command=self.on_click_pay_all)
        pay_all_btn.place(x=210, y=440, width=100, height=30)
        pay_btn = ttk.Button(charges_frame, text="Pay", command=self.on_click_pay)
        pay_btn.place(x=320, y=440, width=100, height=30)

        # Footer
        cancel_btn = ttk.Button(top, text='Back', command=lambda: self.top.destroy())
        cancel_btn.place(x=200, y=640, width=100, height=40)

        self.charge_tree.bind("<<TreeviewSelect>>", self.on_click_details)

    def refresh_table(self, data_list=None):
        for data in self.charge_tree.get_children():
            self.charge_tree.delete(data)
        self.charge_detail['text'] = ''
        if data_list is None:
            data_list = db.rental_handler.get_rental_by_uid(self.uid, status="paying")
            data_list.reverse()
        total = 0
        for data in data_list:
            from utils.datetime_utils import get_total_hours
            if data['status'] == "inuse":
                continue
            duration, _ = get_total_hours(data['starttime'], data['endtime'])
            value = (data['id'],
                     f"{data['loc_from']}->{data['loc_to']}",
                     duration,
                     f"£{data['billtotal']}",
                     data["status"])
            self.charge_tree.insert(parent='', index='end', text='', values=value)
            if data['status'] == "paying":
                total += data['billtotal']
        self.total_message["text"] = f"Total Remaining Charge: £{total}"

    def on_click_pay(self):
        try:
            selected_item = self.charge_tree.selection()[0]
            values = self.charge_tree.item(selected_item)['values']
            rental_id = values[0]
            status = values[-1]
            if status == "done":
                messagebox.showinfo("Info", "You have paid for this rental")
            else:
                rental = db.rental_handler.get_rental_info_by_id(rental_id)
                rental['status'] = 'done'
                bill_total = round(rental['billtotal'], 2)

                user = db.user_handler.get_user_info_by_id(rental['uid'])

                if bill_total > user['balance']:
                    messagebox.showerror("Error", "Your balance is not enough")
                else:
                    db.user_handler.update_user_by_id(rental['uid'],
                                                      fields={'balance': round(user['balance'] - bill_total, 2)})
                    db.rental_handler.update_rental(rent_id=rental['id'], fields=rental)
                    self.balance_label['text'] = f"Current Balance: £{user['balance'] - bill_total}"
                    self.refresh_table()
        except IndexError:
            messagebox.showerror("Error", "No rental selected")

    def on_click_pay_all(self):
        unpaid_rentals = db.rental_handler.get_rental_by_uid(self.uid, status="paying")
        if len(unpaid_rentals) == 0:
            messagebox.showinfo("Info", "You have no remaining charge")
        else:
            total = sum([r['billtotal'] for r in unpaid_rentals])
            total = round(total, 2)
            user = db.user_handler.get_user_info_by_id(self.uid)

            if total > user['balance']:
                messagebox.showerror("Error", "Your balance is not enough")
            else:
                answer = messagebox.askokcancel("Pay All", f"Are you sure to pay all remaining charge £({total})?")
                if answer:
                    db.user_handler.update_user_by_id(self.uid, fields={'balance': round(user['balance'] - total, 2)})
                    for rental in unpaid_rentals:
                        db.rental_handler.update_rental(rent_id=rental['id'], fields={'status': 'done'})
                    self.balance_label['text'] = f"Current Balance: £{user['balance'] - total}"
                    self.refresh_table()

    def on_click_details(self, event):
        try:
            selected_item = self.charge_tree.selection()[0]
            rental_id = self.charge_tree.item(selected_item)['values'][0]
            rental_obj = db.rental_handler.get_rental_info_by_id(rental_id, return_type='object')
            self.charge_detail["text"], _ = rental_obj.get_detail()
        except IndexError:
            self.charge_detail["text"] = "You have no remaining charge"

    def on_click_show(self, show_all=True):
        if show_all:
            data = db.rental_handler.get_rental_by_uid(self.uid)
            self.refresh_table(data)
            self.show_btn.configure(text="Show Unpaid", command=lambda: self.on_click_show(False))
        else:
            self.refresh_table()
            self.show_btn.configure(text="Show All", command=lambda: self.on_click_show(True))

    def on_click_topup(self):
        from frames.dialogs import TopupDialog
        topup_dialog = TopupDialog(self.top, self.uid)
        self.top.wait_window(topup_dialog.top)
        user = db.user_handler.get_user_info_by_id(self.uid)
        self.balance_label['text'] = f"Current Balance: £{user['balance']}"

    def on_click_topup_history(self):
        from frames.dialogs import TopupHistoryDialog
        topup_history_dialog = TopupHistoryDialog(self.top, self.uid)
        self.top.wait_window(topup_history_dialog.top)

