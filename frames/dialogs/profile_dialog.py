import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import tkintermapview

from utils.const import *
import utils.db_utils as db

class ProfileDialog(object):
    def __init__(self, parent):
        self.uid = parent.uid
        top = self.top = tk.Toplevel(parent)

        self.top.geometry("400x350")
        self.top.title("Profile")

        label = ttk.Label(top, text="Edit Profile", font=LARGEFONT, anchor="center")
        label.place(x=50, y=30, width=300, height=50)

        username_label = ttk.Label(top, text="Username", anchor="e")
        username_label.place(x=10, y=100, width=110, height=30)

        self.username = ttk.Entry(top)
        self.username.place(x=130, y=100, width=230, height=30)

        password_label = ttk.Label(top, text="Password", anchor="e")
        password_label.place(x=10, y=140, width=110, height=30)

        self.password = ttk.Entry(top, show="*")
        self.password.place(x=130, y=140, width=230, height=30)

        dob_label = ttk.Label(top, text="D.O.B", anchor="e")
        dob_label.place(x=10, y=180, width=110, height=30)

        self.dob_variable = tk.StringVar()
        self.dob = DateEntry(top, textvariable=self.dob_variable)
        self.dob.delete(0, "end")
        self.dob.place(x=130, y=180, width=230, height=30)

        phone_label = ttk.Label(top, text="Phone Number", anchor="e")
        phone_label.place(x=10, y=220, width=110, height=30)

        self.phone = ttk.Entry(top)
        self.phone.place(x=130, y=220, width=230, height=30)

        submit_btn = ttk.Button(top, text="Submit",
                                command=self.on_submit)
        submit_btn.place(x=125, y=270, width=150, height=30)

        back_btn = ttk.Button(top, text="Cancel",
                              command=lambda: self.top.destroy())
        back_btn.place(x=125, y=310, width=150, height=30)

        user = db.user_handler.get_user_info_by_id(self.uid)

        self.username.insert(0, user.get('username'))
        self.password.insert(0, user.get('password'))
        self.dob_variable.set(user.get('dob'))
        self.phone.insert(0, user.get('phone'))

        self.username.config(state="disabled")

    def on_submit(self):
        user = db.user_handler.get_user_info_by_id(self.uid)

        password = self.password.get()
        dob = self.dob_variable.get()
        phone = self.phone.get()

        old_pass = simpledialog.askstring("Confirm old password", "Please type in your current password", show="*")
        if old_pass is None:
            pass
        elif old_pass != user['password']:
            messagebox.showerror('Error', 'Incorrect Password')
        else:
            user['password'] = password
            user['dob'] = dob
            user['phone'] = phone

            db.user_handler.update_user_by_id(self.uid, fields=user)
            messagebox.showinfo("Info", "Your profile has been updated")
