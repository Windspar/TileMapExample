import tkinter as tk

# store everything in json files

class MapSettings:
    def __init__(self):
        self.tilesize = 0, 0
        self.mapsize = 0, 0

    def build_map(self):
        self.map_data = [[0 for w in range(self.mapsize[0])] for h in range(self.mapsize[1])]

    def load(self):
        pass

    def save(self):
        pass

class MapBuilder:
    def __init__(self):
        self.root = tk.Tk()
        self.settings = MapSettings()
        # Menubar
        self.menubar = tk.Menu(self.root)
        self.pages = tk.Menu(self.menubar, tearoff=0)
        self.pages.add_command(label="WelcomePage", command=self.menu_welcome)
        self.pages.add_command(label="SettingPage", command=self.menu_settings)
        self.menubar.add_cascade(label="Page", menu=self.pages)

        self.root.config(menu=self.menubar)

        # Stacking Panels
        self.container = tk.Frame(self.root)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (WelcomePage, SettingPage):
            page_name = F.__name__
            frame = F(self.container, self)
            frame.frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = frame

        #self.show_frame("WelcomePage")
        self.show_frame("SettingPage")

        self.root.mainloop()

    def show_frame(self, page_name):
        self.frames[page_name].frame.tkraise()

    def menu_welcome(self):
        self.show_frame("WelcomePage")

    def menu_settings(self):
        self.show_frame("SettingPage")

class WelcomePage:
    def __init__(self, parent, handler):
        self.handler = handler
        self.frame = tk.Frame(parent)
        self.label = tk.Label(self.frame, text="Welcome to Map Builder")
        self.label.pack(side="top", pady=10)

class SettingPage:
    def __init__(self, parent, handler):
        self.handler = handler
        self.frame = tk.Frame(parent)
        self.label = tk.Label(self.frame, text="Map Settings")
        self.label.pack(side="top", pady=10)

MapBuilder()
