import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import utils.db_utils as db
from utils.const import LARGEFONT

class ManagerFunctionsFrame(tk.Frame):
    def __init__(self, parent, controller):
        from frames import ManagerFrame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.uid = controller.uid
        self.user_info = db.user_handler.get_user_info_by_id(self.uid)

        self.win_size = "1000x700"
        self.tree = ttk.Treeview(self)
        self.tree.place(x=20, y=350, width=800, height=330)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.place(x=820, y=350, width=10, height=330)
        self.tree.configure(yscrollcommand=scrollbar.set)

        label = ttk.Label(self, text=f"Hi, {self.user_info['username']}",
                          font=LARGEFONT, anchor="w")
        label.place(x=20, y=10, width=500, height=50)

        back_btn = ttk.Button(self, text="Back",
                              command=lambda: self.controller.show_frame(ManagerFrame))
        back_btn.place(x=900, y=20, width=80, height=40)

        manager_menu_frame = ttk.Labelframe(self, text='Menu')
        manager_menu_frame.place(x=20, y=90, width=800, height=75)

        user_btn = ttk.Button(manager_menu_frame, text="Manage Users",
                              command=lambda: self.controller.show_frame(ManagerUserFrame))
        vehicle_btn = ttk.Button(manager_menu_frame, text="Manage Vehicles",
                                 command=lambda: self.controller.show_frame(ManagerVehicleFrame))

        user_btn.place(x=50, y=0, width=220, height=50)
        vehicle_btn.place(x=300, y=0, width=220, height=50)

        add_btn = ttk.Button(self, text="Add", command=self.add)
        add_btn.place(x=840, y=190, width=150, height=70)

        update_btn = ttk.Button(self, text="Update", command=self.update)
        update_btn.place(x=840, y=270, width=150, height=70)

        delete_btn = ttk.Button(self, text="Delete", command=self.delete)
        delete_btn.place(x=840, y=350, width=150, height=70)

        search_btn = ttk.Button(self, text="Search", command=self.search)
        search_btn.place(x=840, y=430, width=150, height=70)

        reset_btn = ttk.Button(self, text="Reset", command=self.reset)
        reset_btn.place(x=840, y=510, width=150, height=70)

    def test(self):
        raise NotImplemented

    def update(self):
        raise NotImplemented

    def add(self):
        raise NotImplemented

    def delete(self):
        raise NotImplemented

    def search(self):
        raise NotImplemented

    def reset(self):
        raise NotImplemented

    def treeview_sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))


class ManagerUserFrame(ManagerFunctionsFrame):
    def __init__(self, parent, controller):
        ManagerFunctionsFrame.__init__(self, parent, controller)

        info_frame = ttk.LabelFrame(self, text='Info')
        info_frame.place(x=20, y=180, width=800, height=140)

        username_label = ttk.Label(info_frame, text='Username', anchor="w")
        userid_label = ttk.Label(info_frame, text='User ID', anchor="w")
        dob_label = ttk.Label(info_frame, text='Date of Birth', anchor="w")
        phone_label = ttk.Label(info_frame, text='Phone Number', anchor="w")
        role_label = ttk.Label(info_frame, text='Role', anchor="w")

        userid_label.place(x=10, y=0, width=100, height=30)
        username_label.place(x=10, y=40, width=100, height=30)
        role_label.place(x=450, y=40, width=100, height=30)
        dob_label.place(x=10, y=80, width=100, height=30)
        phone_label.place(x=450, y=80, width=100, height=30)

        self.username_variable = tk.StringVar()
        self.userid_variable = tk.StringVar()
        self.dob_variable = tk.StringVar()
        self.phone_variable = tk.StringVar()
        self.role_variable = tk.StringVar()

        self.username_entry = ttk.Entry(info_frame, textvariable=self.username_variable)
        self.userid_entry = ttk.Entry(info_frame, state="disabled", textvariable=self.userid_variable)
        self.dob_entry = DateEntry(info_frame, textvariable=self.dob_variable)
        self.dob_entry.delete(0, "end")
        self.phone_entry = ttk.Entry(info_frame, textvariable=self.phone_variable)
        self.role_entry = ttk.Combobox(info_frame, textvariable=self.role_variable)
        self.role_entry['values'] = ['All', 'Customer', 'Operator', 'Manager']
        self.role_entry.current(0)

        self.userid_entry.place(x=110, y=0, width=210, height=30)
        self.username_entry.place(x=110, y=40, width=330, height=30)
        self.role_entry.place(x=580, y=40, width=210, height=30)
        self.dob_entry.place(x=110, y=80, width=330, height=30)
        self.phone_entry.place(x=580, y=80, width=210, height=30)

        self.tree['columns'] = ('User ID', "Username", "D.O.B", "Phone Number", "Balance", "Role")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("User ID", anchor=tk.W, width=100)
        self.tree.column("Username", anchor=tk.W, width=160)
        self.tree.column("D.O.B", anchor=tk.W, width=160)
        self.tree.column("Phone Number", anchor=tk.W, width=180)
        self.tree.column("Balance", anchor=tk.W, width=100)
        self.tree.column("Role", anchor=tk.W, width=100)

        self.tree.heading("User ID", text="User ID", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("User ID", False))
        self.tree.heading("Username", text="Username", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("Username", False))
        self.tree.heading("D.O.B", text="D.O.B", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("D.O.B", False))
        self.tree.heading("Phone Number", text="Phone Number", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("Phone Number", False))
        self.tree.heading("Balance", text="Balance", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("Balance", False))
        self.tree.heading("Role", text="Role", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("Role", False))

        self.refresh_table()
        self.tree.bind("<<TreeviewSelect>>", self.on_click)

    def on_click(self, event):
        selected_item = self.tree.selection()[0]
        self.username_variable.set(self.tree.item(selected_item)['values'][1])
        self.userid_variable.set(self.tree.item(selected_item)['values'][0])
        self.dob_variable.set(self.tree.item(selected_item)['values'][2])
        self.phone_variable.set(self.tree.item(selected_item)['values'][3])
        self.role_variable.set(self.tree.item(selected_item)['values'][5].capitalize())

    def refresh_table(self, data_list=None):
        for data in self.tree.get_children():
            self.tree.delete(data)
        if data_list is None:
            for data in db.user_handler.get_all_user():
                value = (data['id'], data['username'], data['dob'], data['phone'], data['balance'], data['role'])
                self.tree.insert(parent='', index='end', text="", values=value, tag="orow")
        else:
            for data in data_list:
                value = (data['id'], data['username'], data['dob'], data['phone'], data['balance'], data['role'])
                self.tree.insert(parent='', index='end', text="", values=value, tag="orow")

    def search(self):
        conditions = []

        username = self.username_entry.get()
        if username != '':
            conditions.append(f"username LIKE '%{username}%'")

        role = self.role_entry.get()
        if role != 'All':
            conditions.append(f"role='{role.lower()}'")

        phone = self.phone_entry.get()
        if phone != '':
            conditions.append(f"phone like '%{phone}%'")

        dob = self.dob_variable.get()
        if dob != '':
            conditions.append(f"dob='{phone}'")

        if len(conditions) > 0:
            query = f"SELECT * FROM Users WHERE {' AND '.join(conditions)} AND status='active'"
        else:
            query = "SELECT * FROM Users WHERE status='active'"
        cursor = db.db_handler.cursor
        cursor.execute(query)
        results = cursor.fetchall()
        results = [dict(r) for r in results]

        self.refresh_table(data_list=results)

    def delete(self):
        user_id = self.userid_variable.get()
        if user_id == '':
            messagebox.showerror("Invalid ID")
        else:
            db.user_handler.update_user_by_id(user_id, fields={'status': 'disable'})
            messagebox.showinfo("Success", f"User id {user_id} is deactivated")
            self.reset()

    def add(self):
        username = self.username_variable.get()
        if username == "":
            messagebox.showerror("Error", "Invalid username")
        elif db.user_handler.get_user_by_username(username) is not None:
            messagebox.showerror("Error", "Username existed")
        else:
            password = simpledialog.askstring("Password", "Type in the password for this new user")
            if password is None or password == "":
                messagebox.showwarning("Error", "Invalid password")
            else:
                db.user_handler.create_user(
                    username=username,
                    password=password,
                    dob=self.dob_variable.get(),
                    role=self.role_variable.get().lower() if self.role_variable.get() != "All" else "customer"
                )
                messagebox.showinfo("Success", "New user is added successfully")
                self.reset()

    def update(self):
        user_id = self.userid_variable.get()
        fields = {
            "phone": self.phone_variable.get(),
            "dob": self.dob_variable.get(),
            "role": self.role_variable.get().lower()
        }
        if user_id == "":
            messagebox.showerror("Error", "No user selected")
        else:
            db.user_handler.update_user_by_id(user_id, fields=fields)
            messagebox.showinfo("Success", "User Updated")
            self.reset()

    def reset(self):
        self.role_entry.current(0)
        self.username_entry.delete(0, 'end')
        self.userid_entry.delete(0, 'end')
        self.dob_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.refresh_table()


class ManagerVehicleFrame(ManagerFunctionsFrame):
    def __init__(self, parent, controller):
        ManagerFunctionsFrame.__init__(self, parent, controller)

        info_frame = ttk.LabelFrame(self, text='Info')
        info_frame.place(x=20, y=180, width=800, height=140)

        id_label = ttk.Label(info_frame, text='Vehicle ID', anchor="w")
        type_label = ttk.Label(info_frame, text='Type', anchor="w")
        location_label = ttk.Label(info_frame, text='Location', anchor="w")
        battery_label = ttk.Label(info_frame, text='Battery', anchor="w")
        status_label = ttk.Label(info_frame, text='Status', anchor="w")

        id_label.place(x=10, y=0, width=100, height=30)
        type_label.place(x=10, y=40, width=100, height=30)
        status_label.place(x=450, y=40, width=100, height=30)
        location_label.place(x=10, y=80, width=100, height=30)
        battery_label.place(x=450, y=80, width=100, height=30)

        self.type_variable = tk.StringVar()
        self.id_variable = tk.StringVar()
        self.location_variable = tk.StringVar()
        self.battery_variable = tk.StringVar()
        self.status_variable = tk.StringVar()

        self.id_entry = ttk.Entry(info_frame, state="disabled", textvariable=self.id_variable)
        self.type_entry = ttk.Combobox(info_frame, textvariable=self.type_variable)
        self.location_entry = ttk.Entry(info_frame, textvariable=self.location_variable)
        self.battery_entry = ttk.Entry(info_frame, textvariable=self.battery_variable)
        self.status_entry = ttk.Combobox(info_frame, textvariable=self.status_variable)

        self.type_entry['values'] = ['All', 'Bike', 'Scooter']
        self.type_entry.current(0)

        self.status_entry['values'] = ['All', 'Available', 'Unavailable', "Defective"]
        self.status_entry.current(0)

        self.id_entry.place(x=110, y=0, width=210, height=30)
        self.type_entry.place(x=110, y=40, width=330, height=30)
        self.status_entry.place(x=580, y=40, width=210, height=30)
        self.location_entry.place(x=110, y=80, width=330, height=30)
        self.battery_entry.place(x=580, y=80, width=210, height=30)

        self.tree['columns'] = ('Vehicle ID', "Type", "Location", "Battery", "Status")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Vehicle ID", anchor=tk.W, width=120)
        self.tree.column("Type", anchor=tk.W, width=160)
        self.tree.column("Location", anchor=tk.W, width=280)
        self.tree.column("Battery", anchor=tk.W, width=120)
        self.tree.column("Status", anchor=tk.W, width=120)

        self.tree.heading("Vehicle ID", text="User ID", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("Vehicle ID", False))
        self.tree.heading("Type", text="Type", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("Type", False))
        self.tree.heading("Location", text="Location", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("Location", False))
        self.tree.heading("Battery", text="Battery", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("Battery", False))
        self.tree.heading("Status", text="Status", anchor=tk.W,
                          command=lambda: self.treeview_sort_column("Status", False))

        self.refresh_table()
        self.tree.bind("<<TreeviewSelect>>", self.on_click)

    def on_click(self, event):
        selected_item = self.tree.selection()[0]

        self.type_variable.set(self.tree.item(selected_item)['values'][1].capitalize())
        self.id_variable.set(self.tree.item(selected_item)['values'][0])
        self.location_variable.set(self.tree.item(selected_item)['values'][2])
        self.battery_variable.set(self.tree.item(selected_item)['values'][3])
        self.status_variable.set(self.tree.item(selected_item)['values'][4].capitalize())

    def refresh_table(self, data_list=None):
        for data in self.tree.get_children():
            self.tree.delete(data)
        if data_list is None:
            for data in db.vehicle_handler.get_all_vehicles():
                value = (data['id'], data['type'], data['location'], data['battery'], data['status'])
                self.tree.insert(parent='', index='end', text="", values=value, tag="orow")
        else:
            for data in data_list:
                value = (data['id'], data['type'], data['location'], data['battery'], data['status'])
                self.tree.insert(parent='', index='end', text="", values=value, tag="orow")

    def search(self):
        conditions = []

        v_type = self.type_variable.get()
        if v_type != 'All':
            conditions.append(f"type='{v_type.lower()}'")
        status = self.status_variable.get()
        if status != 'All':
            conditions.append(f"status='{status.lower()}'")
        battery = self.battery_variable.get()
        if battery != '':
            conditions.append(f"battery={battery}")
        location = self.location_variable.get()
        if location != '':
            conditions.append(f"location like '%{location}%'")

        if len(conditions) > 0:
            query = f"SELECT * FROM Vehicles WHERE {' AND '.join(conditions)}"
        else:
            query = "SELECT * FROM Vehicles"
        cursor = db.db_handler.cursor
        cursor.execute(query)
        results = cursor.fetchall()
        results = [dict(r) for r in results]
        self.refresh_table(data_list=results)

    def delete(self):
        vehicle_id = self.id_variable.get()
        status = self.status_variable.get()
        if vehicle_id == '':
            messagebox.showerror("Error", "Invalid ID")
        elif status == 'unavailable':
            messagebox.showerror("Error", "This vehicle is being rented")
        else:
            db.vehicle_handler.update_vehicle_by_id(vehicle_id, fields={'status': 'deleted'})
            messagebox.showinfo("Success", f"Vehicle id {vehicle_id} is deleted")
            self.reset()

    def add(self):
        v_type = self.type_variable.get()
        location = self.location_variable.get()
        battery = self.battery_variable.get()

        if v_type == "" or location == "":
            messagebox.showerror("Error", "Please make sure vehicle type and location is provided")
        else:
            db.vehicle_handler.create_vehicle(
                type=v_type.lower(),
                location=location,
                battery=battery if battery != "" else 100,
            )
            messagebox.showinfo("Success", "New vehicle is added successfully")
            self.reset()

    def update(self):
        messagebox.showwarning("Sorry", "Sorry you cannot change Vehicle Information")

    def reset(self):
        self.type_entry.current(0)
        self.id_entry.delete(0, 'end')
        self.location_entry.delete(0, 'end')
        self.battery_entry.delete(0, 'end')
        self.status_entry.current(0)
        self.refresh_table()
