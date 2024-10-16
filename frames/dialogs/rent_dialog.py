import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview

from utils.const import *
import utils.db_utils as db

class RentDialog(object):
    def __init__(self, parent):
        self.uid = parent.uid
        top = self.top = tk.Toplevel(parent)

        self.top.geometry("1000x500")
        self.top.title("Rent")

        map_frame = ttk.LabelFrame(top, text="Map")
        map_frame.place(x=320, y=10, width=670, height=410)

        self.map_widget = tkintermapview.TkinterMapView(map_frame, width=650, height=380)
        self.map_widget.set_address('University of Glasgow')
        self.map_widget.set_zoom(15)
        self.map_widget.pack()

        search_frame = ttk.LabelFrame(top, text="Search")
        search_frame.place(x=10, y=10, width=290, height=480)

        location_label = ttk.Label(search_frame, text='Please select your location', anchor='center')
        location_label.place(x=10, y=0, width=270, height=20)

        self.location_entry = ttk.Entry(search_frame)
        self.location_entry.place(x=10, y=30, width=270, height=30)

        self.location_listbox = tk.Listbox(search_frame, selectmode=tk.BROWSE, exportselection=0)
        self.location_listbox.place(x=10, y=60, width=270, height=170)
        self.update_location_list_box()

        location_yscrollbar = ttk.Scrollbar(search_frame, orient='vertical')
        location_yscrollbar.place(x=270, y=60, width=10, height=170)
        location_yscrollbar.config(command=self.location_listbox.yview)

        vehicle_label = ttk.Label(search_frame, text='Available Vehicles', anchor='center')
        vehicle_label.place(x=10, y=250, width=270, height=20)

        self.vehicle_listbox = tk.Listbox(search_frame, exportselection=0)
        self.vehicle_listbox.place(x=10, y=280, width=270, height=170)

        vehicle_yscrollbar = ttk.Scrollbar(search_frame, orient='vertical')
        vehicle_yscrollbar.place(x=270, y=280, width=10, height=170)
        vehicle_yscrollbar.config(command=self.location_listbox.yview)

        self.rent_btn = ttk.Button(top, text='Rent', command=self.rent)
        self.rent_btn.place(x=340, y=450, width=100, height=30)
        self.cancel_btn = ttk.Button(top, text='Cancel', command=lambda: self.top.destroy())
        self.cancel_btn.place(x=450, y=450, width=100, height=30)

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

        self.map_widget.set_address(location + ", Glasgow")
        # self.map_widget.set_zoom(16)

        self.available_vehicles = db.vehicle_handler.get_vehicles_by_location(location,
                                                                    return_type="object")
        self.vehicle_listbox.delete(0, tk.END)

        for vehicle in self.available_vehicles:
            self.vehicle_listbox.insert(tk.END, str(vehicle))

    def filter_by_string(self, event):
        typed = self.location_entry.get()
        if typed == '':
            self.update_location_list_box()
        else:
            data = [location for location in LOCATION_LIST if typed.lower() in location.lower()]
            self.update_location_list_box(data)

    def rent(self):
        selected_vehicle = self.available_vehicles[self.vehicle_listbox.curselection()[0]]
        if selected_vehicle != "":
            db.rental_handler.create_rental(uid=self.uid, vid=selected_vehicle.id, loc_from=self.location_entry.get())
            db.vehicle_handler.update_vehicle_by_id(vehicle_id=selected_vehicle.id, fields={"status": "unavailable"})
            self.top.destroy()
        else:
            messagebox.showerror("Error", "No vehicle selected")
