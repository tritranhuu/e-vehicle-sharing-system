import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import tkintermapview

import utils.db_utils as db
from utils.const import *
from entities.rental import Rental


class ReturnDialog(object):
    def __init__(self, parent, rental):
        self.uid = parent.uid
        # self.rental = rental
        top = self.top = tk.Toplevel(parent)

        self.top.geometry("1000x500")
        self.top.title("Return")

        map_frame = ttk.LabelFrame(top, text="Map")
        map_frame.place(x=320, y=10, width=670, height=410)

        self.map_widget = tkintermapview.TkinterMapView(map_frame, width=650, height=380)
        self.map_widget.set_address('University of Glasgow')
        self.map_widget.set_zoom(15)
        self.map_widget.pack()

        search_frame = ttk.LabelFrame(top, text="Details")
        search_frame.place(x=10, y=10, width=290, height=480)

        label = ttk.Label(search_frame, text='Here is your rental details', anchor='center')
        label.place(x=10, y=0, width=270, height=20)

        details_message = tk.Message(search_frame)
        details_message.place(x=10, y=30, width=270, height=170)
        details_message.configure(font=('MonoLisa', 10))
        details_message["bg"] = "yellow"
        rental_obj = Rental().load_from_dict(rental)
        details_message["text"], self.rental = rental_obj.get_detail()

        location_label = ttk.Label(search_frame, text='Please select your return location', anchor='center')
        location_label.place(x=10, y=220, width=270, height=20)

        self.location_entry = ttk.Entry(search_frame)
        self.location_entry.place(x=10, y=250, width=270, height=30)

        self.location_listbox = tk.Listbox(search_frame)
        self.location_listbox.place(x=10, y=280, width=270, height=170)
        self.update_location_list_box()

        yscrollbar = ttk.Scrollbar(search_frame, orient='vertical')
        yscrollbar.place(x=270, y=280, width=10, height=170)
        yscrollbar.config(command=self.location_listbox.yview)

        self.confirm_btn = ttk.Button(top, text='Confirm', command=self.on_return)
        self.confirm_btn.place(x=340, y=450, width=100, height=30)
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
        self.map_widget.set_zoom(16)

    def filter_by_string(self, event):
        typed = self.location_entry.get()
        if typed == '':
            self.update_location_list_box()
        else:
            data = [location for location in LOCATION_LIST if typed.lower() in location.lower()]
            self.update_location_list_box(data)

    def on_return(self):
        import random
        return_location = self.location_listbox.get(tk.ANCHOR)
        if return_location == "":
            messagebox.showerror('Error', 'Please choose return location first')
        else:
            vehicle = db.vehicle_handler.get_vehicle_info_by_id(self.rental['vid'])
            vehicle['status'] = 'available'
            vehicle['location'] = return_location
            remain_batt = int(vehicle['battery']-0.2*random.randint(0, int(self.rental['billtotal'])))
            vehicle['battery'] = max(0, remain_batt)
            db.vehicle_handler.update_vehicle_by_id(vehicle_id=self.rental['vid'],
                                                 fields=vehicle)
            self.rental['loc_to'] = return_location
            db.rental_handler.update_rental(rent_id=self.rental['id'], fields=self.rental)

            self.top.destroy()