import tkinter as tk
from tkinter import ttk, messagebox
import utils.db_utils as db
from utils.const import LARGEFONT


class CustomerFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.uid = controller.uid
        self.user_info = db.user_handler.get_user_info_by_id(self.uid)

        self.win_size = "350x500"

        label = ttk.Label(self, text=f"Hi {self.user_info['username']}",
                          font=LARGEFONT, anchor="w")
        label.place(x=10, y=10, width=230, height=50)

        edit_btn = ttk.Button(self, text="Profile",
                                  command=self.on_click_profile)
        edit_btn.place(x=260, y=10, width=80, height=30)

        sign_out_btn = ttk.Button(self, text="Sign out",
                                  command=self.on_click_logout)
        sign_out_btn.place(x=260, y=50, width=80, height=30)

        rent_btn = ttk.Button(self, text="Rent",
                              command=self.on_click_rent)
        rent_btn.place(x=75, y=150, width=200, height=50)

        return_btn = ttk.Button(self, text="Return",
                                command=self.on_click_return)
        return_btn.place(x=75, y=220, width=200, height=50)

        report_btn = ttk.Button(self, text="Report",
                                command=self.on_click_report)
        report_btn.place(x=75, y=290, width=200, height=50)

        pay_btn = ttk.Button(self, text="Pay",
                             command=self.on_click_pay)
        pay_btn.place(x=75, y=360, width=200, height=50)

    def on_click_edit(self):
        pass

    def on_click_return(self):
        current_rental = db.rental_handler.get_rental_by_uid(self.uid, status="inuse")
        if len(current_rental) != 1:
            messagebox.showerror("Error", "You are not renting any vehicle")
        else:
            from frames.dialogs import ReturnDialog
            return_dialog = ReturnDialog(self.controller, current_rental[0])
            self.controller.wait_window(return_dialog.top)

    def on_click_rent(self):
        current_rental = db.rental_handler.get_rental_by_uid(self.uid, status="inuse")
        paying_rentals = db.rental_handler.get_rental_by_uid(self.uid, status="paying")
        if len(current_rental) == 1:
            messagebox.showerror("Error", "You can only rent 1 vehicle at a time")
        elif sum([r['billtotal'] for r in paying_rentals]) > 20:
            messagebox.showerror("Error", "You have an outstanding balance of over £20. "
                                          "Please make the payment to proceed with the rental.")
        else:
            from frames.dialogs import RentDialog
            rent_dialog = RentDialog(self.controller)
            self.controller.wait_window(rent_dialog.top)

    def on_click_pay(self):
        from frames.dialogs import PayDialog
        pay_dialog = PayDialog(self.controller)
        self.controller.withdraw()
        self.controller.wait_window(pay_dialog.top)
        self.controller.deiconify()

    def on_click_report(self):
        from frames.dialogs import ReportDialog
        report_dialog = ReportDialog(self.controller)
        self.controller.withdraw()
        self.controller.wait_window(report_dialog.top)
        self.controller.deiconify()

    def on_click_logout(self):
        from frames import LoginFrame
        answer = messagebox.askokcancel("Question", "Are you sure you want to sign out")
        if answer:
            self.controller.uid = None
            self.controller.show_frame(LoginFrame)

    def on_click_profile(self):
        from frames.dialogs import ProfileDialog
        profile_dialog = ProfileDialog(self.controller)
        self.controller.wait_window(profile_dialog.top)