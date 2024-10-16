import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

import utils.db_utils as db
from frames import LoginFrame
from utils.const import LARGEFONT

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import datetime
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})


class ManagerFrame(tk.Frame):
    def __init__(self, parent, controller):
        from frames import ManagerUserFrame
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.win_size = "1000x800"
        self.con = db.db_handler.db

        self.uid = controller.uid
        self.user_info = db.user_handler.get_user_info_by_id(self.uid)
        label = ttk.Label(self, text=f"Hi {self.user_info['username']}",
                          font=LARGEFONT, anchor="w")
        label.place(x=20, y=10, width=500, height=50)

        back_btn = ttk.Button(self, text="Log out",
                              command=lambda: self.controller.show_frame(LoginFrame))
        back_btn.place(x=850, y=20, width=100, height=50)

        back_btn = ttk.Button(self, text="Manage Database",
                              command=lambda: self.controller.show_frame(ManagerUserFrame))
        back_btn.place(x=700, y=20, width=130, height=50)

        # Chart picking Menu
        graph_menu_frame = ttk.LabelFrame(self, text="Diagram")
        graph_menu_frame.place(x=20, y=90, width=960, height=70)

        revenue_btn = ttk.Button(graph_menu_frame, text="Revenue", command=self.show_revenue)
        revenue_btn.place(x=20, y=0, width=160, height=40)

        trip_btn = ttk.Button(graph_menu_frame, text="Trip Count", command=self.show_vehicle_trip_count)
        trip_btn.place(x=210, y=0, width=160, height=40)

        duration_btn = ttk.Button(graph_menu_frame, text="Rent Duration", command=self.show_rental_duration)
        duration_btn.place(x=400, y=0, width=160, height=40)

        status_btn = ttk.Button(graph_menu_frame, text="Vehicle Status", command=self.show_vehicle_status)
        status_btn.place(x=590, y=0, width=160, height=40)

        battery_btn = ttk.Button(graph_menu_frame, text="Vehicle Battery", command=self.show_vehicle_battery)
        battery_btn.place(x=780, y=0, width=160, height=40)

        # Frame to config the diagram properties
        chart_config_frame = ttk.LabelFrame(self, text="Properties")
        chart_config_frame.place(x=20, y=170, width=960, height=120)

        # Choose period, chart kind, combining vehicle or not for visualization
        sort_label = ttk.Label(chart_config_frame, text="Period")
        sort_label.place(x=20, y=10, width=60, height=30)
        self.period_variable = tk.StringVar()
        self.period_entry = ttk.Combobox(chart_config_frame, textvariable=self.period_variable)
        self.period_entry['values'] = ['Daily', 'Weekly', 'Monthly', 'Yearly']
        self.period_entry.current(0)
        self.period_entry.place(x=80, y=10, width=120, height=30)

        kind_label = ttk.Label(chart_config_frame, text="Chart")
        kind_label.place(x=240, y=10, width=60, height=30)
        self.kind_variable = tk.StringVar()
        self.kind_entry = ttk.Combobox(chart_config_frame, textvariable=self.kind_variable)
        self.kind_entry['values'] = ['line', 'bar']
        self.kind_entry.current(0)
        self.kind_entry.place(x=300, y=10, width=120, height=30)

        combined_label = ttk.Label(chart_config_frame, text="Combine")
        combined_label.place(x=460, y=10, width=60, height=30)
        self.combined_variable = tk.StringVar()
        self.combined_entry = ttk.Combobox(chart_config_frame, textvariable=self.combined_variable)
        self.combined_entry['values'] = ['Yes', 'No']
        self.combined_entry.current(0)
        self.combined_entry.place(x=520, y=10, width=120, height=30)

        # Time period picking
        start_label = ttk.Label(chart_config_frame, text="Start date")
        start_label.place(x=20, y=60, width=60, height=30)
        self.start_variable = tk.StringVar()
        self.start_entry = DateEntry(chart_config_frame, textvariable=self.start_variable,
                                     width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_entry.set_date(datetime.datetime.now() - datetime.timedelta(days=30))
        self.start_entry.place(x=80, y=60, width=120, height=30)

        end_label = ttk.Label(chart_config_frame, text="End date")
        end_label.place(x=240, y=60, width=60, height=30)
        self.end_variable = tk.StringVar()
        self.end_entry = DateEntry(chart_config_frame, textvariable=self.end_variable,
                                   width=12, background='darkblue', foreground='white', borderwidth=2)
        self.end_entry.set_date(datetime.datetime.now())
        self.end_entry.place(x=300, y=60, width=120, height=30)

        show_btn = ttk.Button(chart_config_frame, text="Show", command=self.update_diagram)
        show_btn.place(x=800, y=10, width=120, height=80)

        # Area to show the diagram
        chart_frame = ttk.LabelFrame(self, text="Diagram")
        chart_frame.place(x=20, y=310, width=960, height=460)
        plt.tight_layout()

        self.figure = plt.Figure(figsize=(9.2, 4.4), dpi=100)
        self.chart = FigureCanvasTkAgg(self.figure, chart_frame)
        self.chart.get_tk_widget().pack(pady=20)

        self.cur_func = self.show_revenue
        self.cur_func()

    def show_revenue(self):
        # Set editable properties
        self.figure.clear()
        self.cur_func = self.show_revenue
        self.period_entry.configure(state="enable")
        self.combined_entry.configure(state="enable")
        self.start_entry.configure(state="enable")
        self.end_entry.configure(state="enable")
        self.kind_entry.configure(state="enable")
        self.kind_entry['values'] = ['line', 'bar', 'bar (no trend)', 'pie']
        ax1 = self.figure.add_subplot(111)

        # get variables
        sort_by = self.period_variable.get()
        kind = self.kind_variable.get()
        start = self.start_variable.get()
        start = datetime.datetime.strptime(start, '%m/%d/%y').date()
        end = self.end_variable.get()
        end = datetime.datetime.strptime(end, '%m/%d/%y').date()

        # query and save as a dataframe
        query = f"""SELECT * FROM Rentals r, Vehicles v WHERE r.vid=v.id AND NOT r.status='inuse' AND 
            endtime BETWEEN '{start.strftime('%Y-%m-%dT%H:%M:%S.%f')}' AND '{end.strftime('%Y-%m-%dT%H:%M:%S.%f')}'"""
        rentals = pd.read_sql_query(query,
                                    self.con)
        rentals = rentals[['endtime', 'billtotal', 'type']]

        duration = pd.DataFrame(columns=rentals.columns)
        total_revenue = round(rentals['billtotal'].sum(), 2)

        duration['endtime'] = pd.date_range(start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
        duration['billtotal'] = 0
        duration['type'] = 'bike'

        rentals = pd.concat([rentals, duration])
        rentals["endtime"] = pd.to_datetime(rentals['endtime'], format="%Y-%m-%dT%H:%M:%S.%f")
        rentals.sort_values(by='endtime')
        rentals["endtime"] = rentals['endtime'].dt.to_period(sort_by[0])

        # visualize
        if kind == "pie":
            income = rentals['billtotal'].groupby([rentals['type']]).sum()
            income.plot(kind=kind, ax=ax1, autopct='%1.1f%%')

            ax1.title.set_text(f'Vehicle Type Revenue Percentage from {self.start_variable.get()} to {self.end_variable.get()}')
            ax1.set_ylabel("")

        elif kind == "bar (no trend)":
            income = rentals['billtotal'].groupby([rentals['type']]).sum()
            income.plot(kind='bar', ax=ax1, rot=0, color=['#3DC5FF', '#FF8243'])
            ax1.title.set_text(
                f'Total Revenue from {self.start_variable.get()} to {self.end_variable.get()}')
            ax1.set_ylabel("Revenue (£)")
            ax1.set_xlabel("Vehicle Type")
        else:
            if self.combined_variable.get() == "Yes":
                income = rentals['billtotal'].groupby([rentals['endtime']]).sum()
                legend = False
            else:
                income = rentals['billtotal'].groupby([rentals['endtime'], rentals['type']]).sum().unstack()
                legend = True
                if 'scooter' not in income.columns:
                    income['scooter'] = 0

            sorted_idx = income.index.sort_values()
            income = income.loc[sorted_idx]
            income = income.fillna(0)

            if sort_by == "Daily":
                income.index = income.index.map(lambda x: x.strftime("%d-%m-%Y"))
                ax1.set_xlabel("Date")
            elif sort_by == "Weekly":
                income.index = income.index.map(lambda x: x.strftime("%d-%m-%Y"))
                ax1.set_xlabel("Week")
            elif sort_by == "Monthly":
                income.index = income.index.map(lambda x: x.strftime("%b-%Y"))
                ax1.set_xlabel("Month")
            elif sort_by == "Yearly":
                income.index = income.index.map(lambda x: x.strftime("%Y"))
                ax1.set_xlabel("Year")

            income.plot(kind=kind, legend=legend, ax=ax1, rot=30)

            ax1.title.set_text(f'{sort_by} Revenue from {self.start_variable.get()} to {self.end_variable.get()}\nTotal Revenue: £{total_revenue}')
            ax1.set_ylabel("Revenue (£)")
            ax1.set_xlabel("Time")
        self.chart.draw_idle()

    def show_vehicle_trip_count(self):
        self.figure.clear()
        self.cur_func = self.show_vehicle_trip_count
        self.period_entry.configure(state="enable")
        self.combined_entry.configure(state="enable")
        self.start_entry.configure(state="enable")
        self.end_entry.configure(state="enable")
        self.kind_entry.configure(state="enable")
        self.kind_entry['values'] = ['line', 'bar', 'bar (no trend)', 'pie']

        sort_by = self.period_variable.get()
        kind = self.kind_variable.get()
        start = self.start_variable.get()
        start = datetime.datetime.strptime(start, '%m/%d/%y').date()
        end = self.end_variable.get()
        end = datetime.datetime.strptime(end, '%m/%d/%y').date()

        query = f"""SELECT * FROM Rentals r, Vehicles v WHERE r.vid=v.id AND NOT r.status='inuse' AND 
            endtime BETWEEN '{start.strftime('%Y-%m-%dT%H:%M:%S.%f')}' AND '{end.strftime('%Y-%m-%dT%H:%M:%S.%f')}'"""
        rentals = pd.read_sql_query(query, self.con)
        rentals["endtime"] = pd.to_datetime(rentals['endtime'],
                                            format="%Y-%m-%dT%H:%M:%S.%f")
        total_trip = rentals['endtime'].count()
        ax1 = self.figure.add_subplot(111)
        if kind == "pie":
            count = pd.value_counts(rentals['type'])
            count.plot(kind=kind, ax=ax1, rot=0, autopct='%1.1f%%')

        elif kind == "bar (no trend)":
            count = pd.value_counts(rentals['type'])
            count.plot(kind='bar', ax=ax1, rot=0, color=['#3DC5FF', '#FF8243'])
            ax1.set_ylabel("Number of trips")
            ax1.set_xlabel("Vehicle Type")
        else:
            rentals = rentals[['endtime', 'billtotal', 'type', 'vid']]

            duration = pd.DataFrame(columns=rentals.columns)

            duration['endtime'] = pd.date_range(start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
            duration['billtotal'] = 0
            duration['type'] = 'bike'

            rentals = pd.concat([rentals, duration])
            rentals.sort_values(by='endtime')
            rentals["endtime"] = rentals['endtime'].dt.to_period(sort_by[0])

            if self.combined_variable.get() == "Yes":
                count = rentals['vid'].groupby([rentals['endtime']]).count()
                legend = False
            else:
                count = rentals['vid'].groupby([rentals['endtime'], rentals['type']]).count().unstack()
                legend = True
                if 'scooter' not in count.columns:
                    count['scooter'] = 0

            sorted_idx = count.index.sort_values()
            count = count.loc[sorted_idx]
            count = count.fillna(0)

            if sort_by == "Daily":
                count.index = count.index.map(lambda x: x.strftime("%d-%m-%Y"))
                ax1.set_xlabel("Date")
            elif sort_by == "Weekly":
                count.index = count.index.map(lambda x: x.strftime("%d-%m-%Y"))
                ax1.set_xlabel("Week")
            elif sort_by == "Monthly":
                count.index = count.index.map(lambda x: x.strftime("%b-%Y"))
                ax1.set_xlabel("Month")
            elif sort_by == "Yearly":
                count.index = count.index.map(lambda x: x.strftime("%Y"))
                ax1.set_xlabel("Year")

            count.plot(kind=kind, legend=legend, ax=ax1, rot=30)

            ax1.title.set_text(f'{sort_by} Trip Count from {self.start_variable.get()} to {self.end_variable.get()}\nTotal: {total_trip} trips')
            ax1.set_ylabel("Number of trips")
            ax1.set_xlabel("Time")

        # ax1.title.set_text(f'Trip count by Vehicle')

        self.chart.draw_idle()

    def show_rental_duration(self):
        self.figure.clear()
        self.cur_func = self.show_rental_duration
        self.period_entry.configure(state="enable")
        self.combined_entry.configure(state="enable")
        self.start_entry.configure(state="enable")
        self.end_entry.configure(state="enable")
        self.kind_entry.configure(state="enable")
        self.kind_entry['values'] = ['line', 'bar', 'bar (no trend)', 'pie']

        period = self.period_variable.get()
        kind = self.kind_variable.get()

        start = self.start_variable.get()
        start = datetime.datetime.strptime(start, '%m/%d/%y').date()
        end = self.end_variable.get()
        end = datetime.datetime.strptime(end, '%m/%d/%y').date()

        query = f"""SELECT * FROM Rentals r, Vehicles v WHERE r.vid=v.id AND NOT r.status='inuse' AND 
            endtime BETWEEN '{start.strftime('%Y-%m-%dT%H:%M:%S.%f')}' AND '{end.strftime('%Y-%m-%dT%H:%M:%S.%f')}'"""
        rentals = pd.read_sql_query(query, self.con)
        rentals["endtime"] = pd.to_datetime(rentals['endtime'],
                                            format="%Y-%m-%dT%H:%M:%S.%f")
        rentals["starttime"] = pd.to_datetime(rentals['starttime'],
                                            format="%Y-%m-%dT%H:%M:%S.%f")
        rentals['duration'] = (rentals["endtime"] - rentals["starttime"]).dt.total_seconds()/3600.0

        ax1 = self.figure.add_subplot(111)
        if kind == "pie":
            duration = rentals['duration'].groupby([rentals['type']]).sum()
            duration.plot(kind=kind, ax=ax1, autopct='%1.1f%%')

            ax1.title.set_text(
                f'Vehicle Renting Duration Percentage from {self.start_variable.get()} to {self.end_variable.get()}')
            ax1.set_ylabel("")

        elif kind == "bar (no trend)":
            duration = rentals['duration'].groupby([rentals['type']]).sum()
            duration.plot(kind='bar', ax=ax1, rot=0, color=['#3DC5FF', '#FF8243'])
            ax1.title.set_text(
                f'Total Renting Duration from {self.start_variable.get()} to {self.end_variable.get()}')
            ax1.set_ylabel("Duration (hours)")
            ax1.set_ylabel("Vehicle Type")
        else:
            rentals = rentals[['endtime', 'duration', 'type']]

            duration = pd.DataFrame(columns=rentals.columns)

            duration['endtime'] = pd.date_range(start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
            duration['duration'] = 0
            duration['type'] = 'bike'

            rentals = pd.concat([rentals, duration])
            rentals.sort_values(by='endtime')
            rentals["endtime"] = rentals['endtime'].dt.to_period(period[0])

            if self.combined_variable.get() == "Yes":
                duration = rentals['duration'].groupby([rentals['endtime']]).sum()
                legend = False
            else:
                duration = rentals['duration'].groupby([rentals['endtime'], rentals['type']]).sum().unstack()
                legend = True
                if 'scooter' not in duration.columns:
                    duration['scooter'] = 0

            sorted_idx = duration.index.sort_values()
            duration = duration.loc[sorted_idx]
            duration = duration.fillna(0)

            if period == "Daily":
                duration.index = duration.index.map(lambda x: x.strftime("%d-%m-%Y"))
                ax1.set_xlabel("Date")
            elif period == "Weekly":
                duration.index = duration.index.map(lambda x: x.strftime("%d-%m-%Y"))
                ax1.set_xlabel("Week")
            elif period == "Monthly":
                duration.index = duration.index.map(lambda x: x.strftime("%b-%Y"))
                ax1.set_xlabel("Month")
            elif period == "Yearly":
                duration.index = duration.index.map(lambda x: x.strftime("%Y"))
                ax1.set_xlabel("Year")

            duration.plot(kind=kind, legend=legend, ax=ax1, rot=30)

            ax1.title.set_text(f'{period} Renting Duration from {self.start_variable.get()} to {self.end_variable.get()}')
            ax1.set_ylabel("Duration (hours)")
            ax1.set_xlabel("Time")

        self.chart.draw_idle()

    def show_vehicle_status(self):
        self.figure.clear()
        self.cur_func = self.show_vehicle_status

        self.period_entry.configure(state="disable")
        self.start_entry.configure(state="disable")
        self.end_entry.configure(state="disable")
        self.combined_entry.configure(state="enable")
        self.kind_entry.configure(state="enable")
        self.kind_entry['values'] = ['pie', 'bar']

        kind = self.kind_variable.get()
        if kind == "line":
            kind = "pie"
            self.kind_entry.current(0)

        query = "SELECT * FROM Vehicles v WHERE NOT status='deleted'"
        vehicles = pd.read_sql_query(query, self.con)
        if self.combined_variable.get() == "Yes":
            ax1 = self.figure.add_subplot(111)
            count = pd.value_counts(vehicles['status'])
            if kind == "pie":
                count.plot(kind=kind, ax=ax1, rot=0, autopct='%1.1f%%')
            else:
                count.plot(kind=kind, ax=ax1, rot=0)
            ax1.set_ylabel("")
            ax1.title.set_text(f'Vehicle Status Proportion')
        else:
            if kind == "pie":
                ax1 = self.figure.add_subplot(121)
                ax2 = self.figure.add_subplot(122)
                count_bike = pd.value_counts(vehicles[vehicles['type'] == 'bike']['status'])
                count_scooter = pd.value_counts(vehicles[vehicles['type'] == 'bike']['status'])
                count_bike.plot(kind=kind, ax=ax1, rot=0, autopct='%1.1f%%')
                count_scooter.plot(kind=kind, ax=ax2, rot=0, autopct='%1.1f%%')
                ax1.set_ylabel("")
                ax2.set_ylabel("")
                ax1.title.set_text(f'Bike Status Proportion')
                ax2.title.set_text(f'Scooter Status Proportion')
            else:
                ax1 = self.figure.add_subplot(111)
                count = vehicles['id'].groupby([vehicles['status'], vehicles['type']]).count().unstack()
                count.plot(kind=kind, legend=True, ax=ax1, rot=0)
                ax1.set_ylabel("")
                ax1.title.set_text(f'Vehicle Status Proportion')
        self.chart.draw_idle()

    def show_vehicle_battery(self):
        self.figure.clear()
        self.cur_func = self.show_vehicle_battery

        self.period_entry.configure(state="disable")
        self.start_entry.configure(state="disable")
        self.end_entry.configure(state="disable")
        self.combined_entry.configure(state="enable")
        self.kind_entry.configure(state="disable")

        if self.combined_variable.get() == "No":
            ax1 = self.figure.add_subplot(121)
            ax2 = self.figure.add_subplot(122)

            query = "SELECT * FROM Vehicles v WHERE NOT status='deleted'"
            vehicles = pd.read_sql_query(query, self.con)
            battery_bike = vehicles[vehicles['type'] == 'bike']['battery'].to_numpy()
            battery_scooter = vehicles[vehicles['type'] == 'scooter']['battery'].to_numpy()
            ax1.hist(battery_bike, bins=100, color="#2574F4")
            ax1.title.set_text(f'Bike Battery Histogram')
            ax2.hist(battery_scooter, bins=100, color="#08BAB7")
            ax2.title.set_text(f'Scooter Battery Histogram')
        else:
            ax1 = self.figure.add_subplot(111)

            query = "SELECT * FROM Vehicles v WHERE NOT status='deleted'"
            vehicles = pd.read_sql_query(query, self.con)
            battery = vehicles['battery'].to_numpy()
            ax1.hist(battery, bins=100)
            ax1.title.set_text(f'Vehicle Battery Histogram')
        self.chart.draw_idle()

    def update_diagram(self):
        self.cur_func()
