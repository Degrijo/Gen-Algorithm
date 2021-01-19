import tkinter as tk


from constants import ROW_NUMBER, COL_NUMBER, ICONS


WIN_WIDTH = 800
WIN_HEIGHT = 500
WIN_MIN_WIDTH = 700
WIN_MIN_HEIGHT = 300
FIELD_WIDTH = 1575
FIELD_HEIGHT = 1045
IMAGES = {tag: tk.PhotoImage(file=pict) for tag, pict in ICONS.items()}


class View:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+300+150")
        self.root.minsize(WIN_MIN_WIDTH, WIN_MIN_HEIGHT)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        toolbar = tk.Frame(self.root, highlightthickness=1, highlightbackground='black', width=300)
        toolbar.grid(row=0, column=1, sticky='ns', padx=(0, 10), pady=(10, 10))
        self.field = Canvas()
        self.field.grid(row=0, column=0, sticky='nswe', padx=(10, 10), pady=(10, 10))
        xbar = tk.Scrollbar(self.field, orient=tk.HORIZONTAL, command=self.field.xview)
        ybar = tk.Scrollbar(self.field, command=self.field.yview)
        ybar.grid(row=0, column=1, sticky='ns')
        xbar.grid(row=1, column=0, sticky='we')
        self.field.configure(xscrollcommand=xbar.set, yscrollcommand=ybar.set)
        self.state = True
        self.root.attributes("-fullscreen", self.state)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)

    def display(self):
        self.root.mainloop()


class Canvas(tk.Canvas):
    def __init__(self):
        super().__init__(highlightthickness=1, highlightbackground='black', bg='#004d99', width=FIELD_WIDTH,
                         height=FIELD_HEIGHT, scrollregion=(0, 0, FIELD_WIDTH, FIELD_HEIGHT))
        self.square_width = FIELD_WIDTH // COL_NUMBER
        self.square_height = FIELD_HEIGHT // ROW_NUMBER
        for i in range(1, ROW_NUMBER):
            current_y = self.square_height * i
            self.create_line(0, current_y, FIELD_WIDTH, current_y, width=10)
        for i in range(1, COL_NUMBER):
            current_x = self.square_width * i
            self.create_line(current_x, 0, current_x, FIELD_HEIGHT)

    def draw_image(self, x, y, race, tag):
        self.create_image(x*self.square_width, y*self.square_height,  anchor=tk.CENTER, image=ICONS[race], tag=tag)

    def move_top(self, tag):
        self.moveto(tag, y=-self.square_height)

    def move_bottom(self, tag):
        self.moveto(tag, y=+self.square_height)

    def move_right(self, tag):
        self.moveto(tag, x=self.square_width)

    def move_left(self, tag):
        self.moveto(tag, x=-self.square_width)

    def delete_image(self, obj):
        self.delete(obj)
