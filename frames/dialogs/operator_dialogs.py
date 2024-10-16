import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime
import tkintermapview

import utils.db_utils as db
from utils.const import *
from entities.rental import Rental


class ChargeDialog(object):
    def __init__(self, parent, vid):

        top = self.top = tk.Toplevel(parent)
        self.vid = vid
        self.completed = False
        vehicle = db.vehicle_handler.get_vehicle_info_by_id(vid)

        self.top.geometry("300x220")
        self.top.title("Charge")

        self.label = ttk.Label(top, text=f"Press START to charge Vehicle {vid}", anchor="center")
        self.label.place(x=50, y=20, width=200, height=30)

        self.progressbar = ttk.Progressbar(top, orient="horizontal", value=vehicle['battery'], length=200, mode="determinate")
        self.progressbar.place(x=50, y=80, width=200, height=40)

        self.start_btn = ttk.Button(top, text="START", command=self.on_click_start)
        self.start_btn.place(x=100, y=140, width=100, height=30)
        self.close_btn = ttk.Button(top, text="Close", command=lambda: self.top.destroy())
        self.close_btn.place(x=100, y=180, width=100, height=30)

    def on_click_start(self):
        vehicle = db.vehicle_handler.get_vehicle_info_by_id(self.vid)
        self.label.config(text="Charging ...")

        for i in range(vehicle['battery'], 101):
            time.sleep(0.01)  # Simulate the time spent for charging
            self.progressbar["value"] = i
            self.top.update_idletasks()

        self.label.config(text=f"Vehicle {self.vid} is now fully charged")
        self.start_btn.config(state="disabled")
        db.vehicle_handler.update_vehicle_by_id(self.vid, fields={'battery': 100})
        self.completed = True

class RepairDialog(object):
    def __init__(self, parent, vid):

        top = self.top = tk.Toplevel(parent)
        self.vid = vid
        self.completed = False

        self.top.geometry("300x380")
        self.top.title("Repair")

        self.label = ttk.Label(top, text=f"Press START to repair Vehicle {vid}", anchor="center")
        self.label.place(x=50, y=20, width=200, height=30)

        report_detail = tk.Message(top, width=250)
        report_detail.place(x=20, y=60, width=260, height=150)
        report_detail.configure(font=('MonoLisa', 10, 'bold'), bg='#F9C7BA', fg='#BC3814')
        report = db.report_handler.get_current_by_vid(vid, return_type="object")
        if report is not None:
            report_detail['text'] = str(report)
        else:
            report_detail['text'] = "No Report Recorded"

        self.progressbar = ttk.Progressbar(top, orient="horizontal",  length=200, mode="determinate")
        self.progressbar.place(x=50, y=230, width=200, height=40)

        self.start_btn = ttk.Button(top, text="START", command=self.on_click_start)
        self.start_btn.place(x=100, y=290, width=100, height=30)
        self.close_btn = ttk.Button(top, text="Close", command=lambda: self.top.destroy())
        self.close_btn.place(x=100, y=330, width=100, height=30)

    def on_click_start(self):
        self.label.config(text="Repairing ...")

        for i in range(101):
            time.sleep(0.025)  # Simulate the time spent for charging
            self.progressbar["value"] = i
            self.top.update_idletasks()

        self.label.config(text=f"Vehicle {self.vid} is repaired")
        self.start_btn.config(state="disabled")
        self.completed = True
        db.vehicle_handler.update_vehicle_by_id(self.vid, fields={'status': 'available'})

class MoveDialog(object):
    def __init__(self, parent, vid):

        top = self.top = tk.Toplevel(parent)
        self.vid = vid
        vehicle = db.vehicle_handler.get_vehicle_info_by_id(vid)
        self.completed = False
        self.location = ""

        self.top.geometry("300x420")
        self.top.title("Move")

        self.label = ttk.Label(top, text=f"Choose location", anchor="center")
        self.label.place(x=10, y=20, width=280, height=30)

        self.location_entry = ttk.Entry(top)
        self.location_entry.place(x=50, y=60, width=200, height=30)

        self.location_listbox = tk.Listbox(top, selectmode=tk.BROWSE, exportselection=0)
        self.location_listbox.place(x=50, y=90, width=200, height=150)
        self.update_location_list_box()

        location_yscrollbar = ttk.Scrollbar(top, orient='vertical')
        location_yscrollbar.place(x=250, y=90, width=10, height=150)
        location_yscrollbar.config(command=self.location_listbox.yview)

        self.progress_label = ttk.Label(top, text=f"Vehicle {vid} is at {vehicle['location']} now", anchor="center")
        self.progress_label.place(x=10, y=270, width=280, height=20)
        self.progressbar = ttk.Progressbar(top, orient="horizontal", length=200, mode="determinate")
        self.progressbar.place(x=50, y=300, width=200, height=20)

        self.start_btn = ttk.Button(top, text="MOVE", command=self.on_click_move)
        self.start_btn.place(x=100, y=340, width=100, height=30)
        self.close_btn = ttk.Button(top, text="Close", command=lambda: self.top.destroy())
        self.close_btn.place(x=100, y=380, width=100, height=30)

        self.location_listbox.bind("<<ListboxSelect>>", self.fill_out)
        self.location_listbox.bind("<B1-Leave>", lambda event: "break")
        self.location_entry.bind("<KeyRelease>", self.filter_by_string)

    def update_location_list_box(self, data=None):
        self.location_listbox.delete(0, tk.END)
        if data is None:
            data = LOCATION_LIST
        for location in data:
            self.location_listbox.insert(tk.END, location)

    def fill_out(self, event):
        self.location_entry.delete(0, tk.END)
        location = self.location_listbox.get(tk.ANCHOR)
        self.location_entry.insert(0, location)


    def filter_by_string(self, event):
        typed = self.location_entry.get()
        if typed == '':
            self.update_location_list_box()
        else:
            data = [location for location in LOCATION_LIST if typed.lower() in location.lower()]
            self.update_location_list_box(data)

    def on_click_move(self):
        location = self.location_entry.get()
        if location not in LOCATION_LIST:
            messagebox.showerror("Error", "Invalid location")
        else:
            self.progressbar["value"] = 0
            self.progress_label.config(text=f"Moving")
            for i in range(101):
                time.sleep(0.01)  # Simulate the time spent for charging
                self.progressbar["value"] = i
                self.top.update_idletasks()
            db.vehicle_handler.update_vehicle_by_id(self.vid, fields={'location': location})
            self.progress_label.config(text=f"Vehicle {self.vid} is at {location} now")
            self.location = location
            self.completed = True


class TrackDialog(object):
    def __init__(self, parent):

        top = self.top = tk.Toplevel(parent)
        self.completed = False
        locations = db.vehicle_handler.get_locations_of_vehicle()
        self.locations = {l['location']: l['num_vehicle'] for l in locations}
        self.location = ""

        self.top.geometry("300x420")
        self.top.title("Track")

        self.label = ttk.Label(top, text=f"Choose location", anchor="center")
        self.label.place(x=10, y=20, width=280, height=30)

        self.location_entry = ttk.Entry(top)
        self.location_entry.place(x=50, y=60, width=200, height=30)

        self.location_listbox = tk.Listbox(top, selectmode=tk.BROWSE, exportselection=0)
        self.location_listbox.place(x=50, y=90, width=200, height=150)
        self.update_location_list_box()

        location_yscrollbar = ttk.Scrollbar(top, orient='vertical')
        location_yscrollbar.place(x=250, y=90, width=10, height=150)
        location_yscrollbar.config(command=self.location_listbox.yview)

        self.vehicle_label = ttk.Label(top, text=f"", anchor="center")
        self.vehicle_label.place(x=10, y=270, width=280, height=20)

        self.start_btn = ttk.Button(top, text="Set Location", command=self.on_click_start)
        self.start_btn.place(x=100, y=340, width=100, height=30)
        self.close_btn = ttk.Button(top, text="Close", command=lambda: self.top.destroy())
        self.close_btn.place(x=100, y=380, width=100, height=30)

        self.location_listbox.bind("<<ListboxSelect>>", self.fill_out)
        self.location_listbox.bind("<B1-Leave>", lambda event: "break")
        self.location_entry.bind("<KeyRelease>", self.filter_by_string)

    def update_location_list_box(self, data=None):
        self.location_listbox.delete(0, tk.END)
        if data is None:
            data = list(self.locations.keys())
        for location in data:
            self.location_listbox.insert(tk.END, location)


    def fill_out(self, event):
        self.location_entry.delete(0, tk.END)
        location = self.location_listbox.get(tk.ANCHOR)
        self.location_entry.insert(0, location)

        self.vehicle_label.config(text=f"There are {self.locations[location]} vehicles in {location} now")


    def filter_by_string(self, event):
        typed = self.location_entry.get()
        if typed == '':
            self.update_location_list_box()
        else:
            data = [location for location in self.locations if typed.lower() in location.lower()]
            self.update_location_list_box(data)

    def on_click_start(self):
        location = self.location_entry.get()
        if location not in self.locations:
            messagebox.showerror("Error", "Invalid location")
        else:
            self.location = location
            self.completed = True
            self.top.destroy()