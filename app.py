from frames import *
import tkinter as tk

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("E-Vehicle Share System")
        self.uid = None

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in [LoginFrame, SignUpFrame]:
            self.add_frame(F)

        self.show_frame(LoginFrame)

    def add_frame(self, F):
        frame = F(self.container, self)
        self.frames[F] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        return self.frames[F]

    def show_frame(self, cont):
        if cont in self.frames:
            frame = self.frames[cont]
        else:
            frame = self.add_frame(cont)
        try:
            self.geometry(frame.win_size)
        except:
            pass
        frame.tkraise()


if __name__ == '__main__':
    app = App()
    app.mainloop()
