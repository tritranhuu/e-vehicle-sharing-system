import tkinter as tk
from tkinter import ttk, messagebox

import utils.db_utils as db
from utils.const import LARGEFONT
from frames import LoginFrame

class OperatorFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.uid = controller.uid
        self.user_info = db.user_handler.get_user_info_by_id(self.uid)

        self.win_size = "1000x560"

        label = ttk.Label(self, text=f"Hi {self.user_info['username']}",
                          font=LARGEFONT, anchor="w")
        label.place(x=10, y=10, width=500, height=50)

        back_btn = ttk.Button(self, text="Log out",
                              command=lambda: self.controller.show_frame(LoginFrame))
        back_btn.place(x=740, y=20, width=80, height=40)

        manager_menu_frame = ttk.Labelframe(self, text='Menu')
        manager_menu_frame.place(x=20, y=70, width=800, height=90)

        self.vehicle_tree = ttk.Treeview(self)
        self.vehicle_tree.place(x=20, y=180, width=800, height=330)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.vehicle_tree.yview)
        scrollbar.place(x=820, y=180, width=10, height=330)
        self.vehicle_tree.configure(yscrollcommand=scrollbar.set)

        track_btn = ttk.Button(manager_menu_frame, text="Track", command=self.on_click_track)
        show_all_btn = ttk.Button(manager_menu_frame, text="Show All", command=self.refresh_table)
        low_battery_btn = ttk.Button(manager_menu_frame, text="Show Low Battery", command=self.on_click_low_battery)
        show_defective_btn = ttk.Button(manager_menu_frame, text="Show Defective", command=self.on_click_defective)

        track_btn.place(x=20, y=10, width=160, height=50)
        show_all_btn.place(x=220, y=10, width=160, height=50)
        low_battery_btn.place(x=420, y=10, width=160, height=50)
        show_defective_btn.place(x=620, y=10, width=160, height=50)

        charge_btn = ttk.Button(self, text="Charge", command=self.on_click_charge)
        repair_btn = ttk.Button(self, text="Repair", command=self.on_click_repair)
        move_btn = ttk.Button(self, text="Move", command=self.on_click_move)

        charge_btn.place(x=840, y=180, width=150, height=70)
        repair_btn.place(x=840, y=260, width=150, height=70)
        move_btn.place(x=840, y=340, width=150, height=70)

        tree_label = ttk.Label(self, text="Operator MENU", anchor="center")
        tree_label.place(x=20, y=520, width=800, height=30)

        self.vehicle_tree['columns'] = ('Vehicle ID', "Type", "Location", "Battery", "Status")

        self.vehicle_tree.column("#0", width=0, stretch=tk.NO)
        self.vehicle_tree.column("Vehicle ID", anchor=tk.W, width=100)
        self.vehicle_tree.column("Type", anchor=tk.W, width=200)
        self.vehicle_tree.column("Location", anchor=tk.W, width=200)
        self.vehicle_tree.column("Battery", anchor=tk.W, width=150)
        self.vehicle_tree.column("Status", anchor=tk.W, width=150)

        self.vehicle_tree.heading("Vehicle ID", text="Vehicle ID", anchor=tk.W,
                                  command=lambda: self.treeview_sort_column("Vehicle ID", False))
        self.vehicle_tree.heading("Type", text="Type", anchor=tk.W,
                                  command=lambda: self.treeview_sort_column("Type", False))
        self.vehicle_tree.heading("Location", text="Location", anchor=tk.W,
                                  command=lambda: self.treeview_sort_column("Location", False))
        self.vehicle_tree.heading("Battery", text="Battery", anchor=tk.W,
                                  command=lambda: self.treeview_sort_column("Battery", False))
        self.vehicle_tree.heading("Status", text="Status", anchor=tk.W,
                                  command=lambda: self.treeview_sort_column("Status", False))

        self.refresh_table()

    def refresh_table(self, data_list=None):
        for data in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(data)

        if data_list is None:
            for data in db.vehicle_handler.get_all_vehicles():
                value = (data['id'], data['type'], data['location'], f"{data['battery']}%", data['status'])
                self.vehicle_tree.insert(parent='', index='end', text="", values=value, tag="orow")
        else:
            for data in data_list:
                value = (data['id'], data['type'], data['location'], f"{data['battery']}%", data['status'])
                self.vehicle_tree.insert(parent='', index='end', text="", values=value, tag="orow")


    def on_click_track(self):
        from frames.dialogs import TrackDialog

        track_dialog = TrackDialog(self.controller)
        self.controller.wait_window(track_dialog.top)
        if track_dialog.completed:
            vehicles = db.vehicle_handler.get_vehicles_by_location(track_dialog.location, status=None)
            self.refresh_table(data_list=vehicles)


    def on_click_low_battery(self):
        data_list = db.vehicle_handler.get_vehicles_by_battery()
        self.refresh_table(data_list)

    def on_click_defective(self):
        data_list = db.vehicle_handler.get_defective_vehicles()
        self.refresh_table(data_list)

    def on_click_charge(self):
        try:
            from frames.dialogs import ChargeDialog
            selected_item = self.vehicle_tree.selection()[0]
            values = self.vehicle_tree.item(selected_item)['values']
            if values[-1] == 'unavailable':
                messagebox.showerror("Error", "This vehicle is on rented")
            else:
                vid = values[0]
                charge_dialog = ChargeDialog(self.controller, vid)
                self.controller.wait_window(charge_dialog.top)
                if charge_dialog.completed:
                    selected = self.vehicle_tree.focus()
                    self.vehicle_tree.item(selected, text="", values=(values[0], values[1], values[2], "100%", values[4]))
        except IndexError:
            messagebox.showerror("Error", "Please select a vehicle")

    def on_click_repair(self):
        try:
            from frames.dialogs import RepairDialog
            selected_item = self.vehicle_tree.selection()[0]
            values = self.vehicle_tree.item(selected_item)['values']
            if values[4] != "defective":
                messagebox.showerror("Error", "This vehicle is not defective")
            else:
                vid = values[0]
                repair_dialog = RepairDialog(self.controller, vid)
                self.controller.wait_window(repair_dialog.top)
                if repair_dialog.completed:
                    selected = self.vehicle_tree.focus()
                    self.vehicle_tree.item(selected, text="", values=(values[0], values[1], values[2], values[3], "available"))
        except IndexError:
            messagebox.showerror("Error", "Please select a vehicle")

    def on_click_move(self):
        try:
            from frames.dialogs import MoveDialog
            selected_item = self.vehicle_tree.selection()[0]
            values = self.vehicle_tree.item(selected_item)['values']
            if values[-1] == 'unavailable':
                messagebox.showerror("Error", "This vehicle is on rented")
            else:
                vid = values[0]
                move_dialog = MoveDialog(self.controller, vid)
                self.controller.wait_window(move_dialog.top)
                if move_dialog.completed:
                    selected = self.vehicle_tree.focus()
                    self.vehicle_tree.item(selected, text="",
                                           values=(values[0], values[1], move_dialog.location, values[3], values[4]))
        except IndexError:
            messagebox.showerror("Error", "Please select a vehicle")

    def treeview_sort_column(self, col, reverse):
        l = [(self.vehicle_tree.set(k, col), k) for k in self.vehicle_tree.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.vehicle_tree.move(k, '', index)
        self.vehicle_tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))


