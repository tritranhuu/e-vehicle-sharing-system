import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

import utils.db_utils as db
from utils.const import LARGEFONT


class SignUpFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.win_size = "400x600"

        tk_image = tk.PhotoImage(file="./data/logo.png")
        img_label = ttk.Label(self, image=tk_image)
        img_label.pack(pady=50)
        img_label.image = tk_image

        label = ttk.Label(self, text="Register", font=LARGEFONT, anchor="center")
        label.place(x=50, y=220, width=300, height=50)

        username_label = ttk.Label(self, text="Username", anchor="e")
        username_label.place(x=10, y=290, width=110, height=30)

        self.username = ttk.Entry(self)
        self.username.place(x=130, y=290, width=230, height=30)

        password_label = ttk.Label(self, text="Password", anchor="e")
        password_label.place(x=10, y=330, width=110, height=30)

        self.password = ttk.Entry(self, show="*")
        self.password.place(x=130, y=330, width=230, height=30)

        re_password_label = ttk.Label(self, text="Confirm Password", anchor="e")
        re_password_label.place(x=10, y=370, width=110, height=30)

        self.re_password = ttk.Entry(self, show="*")
        self.re_password.place(x=130, y=370, width=230, height=30)

        dob_label = ttk.Label(self, text="D.O.B", anchor="e")
        dob_label.place(x=10, y=410, width=110, height=30)

        self.dob_variable = tk.StringVar()
        self.dob = DateEntry(self, textvariable=self.dob_variable)
        self.dob.delete(0, "end")
        self.dob.place(x=130, y=410, width=230, height=30)

        phone_label = ttk.Label(self, text="Phone Number", anchor="e")
        phone_label.place(x=10, y=450, width=110, height=30)

        self.phone = ttk.Entry(self)
        self.phone.place(x=130, y=450, width=230, height=30)

        submit_btn = ttk.Button(self, text="Submit",
                                command=self.create_account)
        submit_btn.place(x=125, y=520, width=150, height=30)

        back_btn = ttk.Button(self, text="Back",
                              command=lambda: controller.show_frame(LoginFrame))
        back_btn.place(x=125, y=560, width=150, height=30)

    def create_account(self):
        username = self.username.get()
        password = self.password.get()
        re_password = self.re_password.get()

        if len(username) < 0:
            messagebox.showerror("Error", "Your username cannot be blank")
        elif password != re_password:
            messagebox.showerror("Error", "Your passwords are not the same")
            self.password.delete(0, tk.END)
            self.re_password.delete(0, tk.END)
        elif len(password) < 8:
            messagebox.showerror("Error", "Your password must have at least 8 characters")
        else:
            user = db.user_handler.get_user_by_username(username)
            if user is not None:
                messagebox.showerror("Error", "Username existed")
                self.username.delete(0, tk.END)
                self.password.delete(0, tk.END)
                self.re_password.delete(0, tk.END)
            else:
                dob = self.dob_variable.get()
                phone = self.phone.get()
                db.user_handler.create_user(username=username, password=password, dob=dob, phone=phone,  role="customer")
                messagebox.showinfo("Congratulations", "Account created successfully")
                self.username.delete(0, tk.END)
                self.password.delete(0, tk.END)
                self.re_password.delete(0, tk.END)
                self.dob.delete(0, tk.END)
                self.phone.delete(0, tk.END)
                self.controller.show_frame(LoginFrame)


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.win_size = "400x600"
        self.controller = controller

        tk_image = tk.PhotoImage(file="./data/logo.png")
        img_label = ttk.Label(self, image=tk_image)
        img_label.pack(pady=50)
        img_label.image = tk_image

        label = ttk.Label(self, text="Login", font=LARGEFONT, anchor="center")
        label.place(x=50, y=220, width=300, height=40)

        role_label = ttk.Label(self, text="Login as:")
        role_label.place(x=40, y=280, width=80, height=30)
        self.role = tk.StringVar()
        rb1 = ttk.Radiobutton(self, text='Customer', variable=self.role, value="customer", )
        rb2 = ttk.Radiobutton(self, text='Operator', variable=self.role, value="operator")
        rb3 = ttk.Radiobutton(self, text='Manager', variable=self.role, value="manager")
        rb1.place(x=40, y=320, width=80, height=40)
        rb2.place(x=150, y=320, width=80, height=40)
        rb3.place(x=260, y=320, width=80, height=40)
        self.role.set("customer")

        username_label = ttk.Label(self, text="Username", anchor="w")
        username_label.place(x=40, y=380, width=80, height=30)

        self.username = ttk.Entry(self)
        self.username.place(x=130, y=380, width=230, height=30)

        password_label = ttk.Label(self, text="Password", anchor="w")
        password_label.place(x=40, y=420, width=80, height=30)

        self.password = ttk.Entry(self, show="*")
        self.password.place(x=130, y=420, width=230, height=30)

        login_btn = ttk.Button(self, text="Sign in",
                               command=self.login)
        login_btn.place(x=125, y=500, width=150, height=30)
        login_btn['state'] = 'active'

        signup_btn = ttk.Button(self, text="Sign up",
                                command=lambda: controller.show_frame(SignUpFrame))

        signup_btn.place(x=125, y=540, width=150, height=30)

    def login(self):
        username = self.username.get()
        password = self.password.get()
        user = db.user_handler.get_user_by_username(username=username)
        if user is None:
            messagebox.showerror("Error", "Username not found!!!")
        else:
            user_id = user['id']
            user_role = user['role']
            if password != user['password']:
                messagebox.showerror("Error", "Incorrect password")
            elif user['status'] != 'active':
                messagebox.showerror("Error", "Your account has been locked")
            else:
                from frames import CustomerFrame, OperatorFrame, ManagerFrame
                self.controller.uid = user_id
                messagebox.showinfo("Congratulations", f"Welcome, {username}")
                if self.role.get() == "operator":
                    if user_role not in ["operator", "manager"]:
                        messagebox.showerror("Error", "Permission denied")
                    else:
                        self.controller.show_frame(OperatorFrame)
                elif self.role.get() == 'manager':
                    if user_role not in ["manager"]:
                        messagebox.showerror("Error", "Permission denied")
                    else:
                        self.controller.show_frame(ManagerFrame)
                else:
                    self.controller.show_frame(CustomerFrame)
