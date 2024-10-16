import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

import utils.db_utils as db

class ReportDialog(object):
    def __init__(self, parent):
        self.uid = parent.uid
        top = self.top = tk.Toplevel(parent)
        self.top.geometry("600x500")
        top.title("Report")

        balance_label = ttk.Label(top, text="Sorry if you have a bad experience", anchor="w")
        balance_label.place(x=20, y=20, width=580, height=20)
        balance_label = ttk.Label(top, text="Noted: You can only report the vehicles you have rented and returned within the past 24 hours", anchor="w")
        balance_label.place(x=20, y=40, width=580, height=20)

        charges_frame = ttk.LabelFrame(top, text="Which vehicle you want to report")
        charges_frame.place(x=20, y=100, width=560, height=300)

        self.charge_tree = ttk.Treeview(charges_frame)
        self.charge_tree.place(x=10, y=10, width=540, height=200)

        self.charge_tree['columns'] = ('Rental ID', 'Vehicle ID', "Type", "Rent On", "Rent At", "")

        self.charge_tree.column("#0", width=0, stretch=tk.NO)
        self.charge_tree.column("Rental ID", anchor=tk.W, width=70)
        self.charge_tree.column("Vehicle ID", anchor=tk.W, width=70)
        self.charge_tree.column("Type", anchor=tk.W, width=50)
        self.charge_tree.column("Rent On", anchor=tk.W, width=120)
        self.charge_tree.column("Rent At", anchor=tk.W, width=160)
        self.charge_tree.column("", anchor=tk.E, width=68)

        self.charge_tree.heading("Rental ID", text="Rental ID", anchor=tk.CENTER)
        self.charge_tree.heading("Vehicle ID", text="Vehicle ID", anchor=tk.CENTER)
        self.charge_tree.heading("Type", text="Type", anchor=tk.CENTER)
        self.charge_tree.heading("Rent On", text="Rent On", anchor=tk.CENTER)
        self.charge_tree.heading("Rent At", text="Rent At", anchor=tk.CENTER)
        self.charge_tree.heading("", text="", anchor=tk.CENTER)

        self.refresh_table()

        pay_btn = ttk.Button(charges_frame, text="Report", command=self.on_click_report)
        pay_btn.place(x=230, y=240, width=100, height=30)

        cancel_btn = ttk.Button(top, text='Back', command=lambda: self.top.destroy())
        cancel_btn.place(x=250, y=440, width=100, height=40)

    def refresh_table(self, data_list=None):
        for data in self.charge_tree.get_children():
            self.charge_tree.delete(data)
        if data_list is None:
            from utils.datetime_utils import beautify_time
            unpaid_rentals = db.rental_handler.get_rental_for_report(self.uid)
            unpaid_rentals.reverse()
            current_report = db.report_handler.get_report_by_uid(self.uid)
            reported_rentals = [r['rid'] for r in current_report]
            reported_vec = []
            for data in unpaid_rentals:
                if data['id'] in reported_rentals:
                    status = "Reported"
                else:
                    status = ""
                if data['vid'] in reported_vec:
                    continue
                reported_vec.append(data['vid'])
                value = (data['id'],
                         data['vid'],
                         data['type'],
                         beautify_time(data['starttime']),
                         data['loc_from'],
                         status)

                self.charge_tree.insert(parent='', index='end', text='', values=value)

    def on_click_report(self):
        selected_item = self.charge_tree.selection()[0]
        values = self.charge_tree.item(selected_item)['values']
        vid = values[1]
        rid = values[0]
        details = simpledialog.askstring("Sorry", "Please provide more details")
        if details is not None:
            db.report_handler.create_report(rid, details)
            db.vehicle_handler.update_vehicle_by_id(vid, fields={'status': 'defective'})
            messagebox.showinfo("Info", "Thank you for reporting")
            self.refresh_table()





