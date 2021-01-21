import tkinter as tk


from constants import ROW_NUMBER, COL_NUMBER, ICONS
# Class Item for canvas obj, View obj return field by default, sorted view init

WIN_WIDTH = 800
WIN_HEIGHT = 500
WIN_MIN_WIDTH = 700
WIN_MIN_HEIGHT = 300
FIELD_WIDTH = 1575
FIELD_HEIGHT = 1045


class View:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+300+150")
        self.root.minsize(WIN_MIN_WIDTH, WIN_MIN_HEIGHT)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        toolbar = tk.Frame(self.root, highlightthickness=1, highlightbackground='black', width=300)
        toolbar.grid(row=0, column=2, sticky='ns', padx=(10, 10), pady=(10, 0))
        self.field = Canvas()
        self.field.grid(row=0, column=0, sticky='nswe', padx=(10, 10), pady=(10, 10))
        xbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.field.xview)
        ybar = tk.Scrollbar(self.root, command=self.field.yview)
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

    def set_controller(self, controller):
        self.root.protocol("WM_DELETE_WINDOW", controller.stop)
        self.root.bind('<space>', controller.run_pause)

    def destroy(self):
        self.root.destroy()

    def display(self):
        self.root.mainloop()


class Canvas(tk.Canvas):
    def __init__(self):
        super().__init__(highlightthickness=1, highlightbackground='black', bg='#004d99', width=FIELD_WIDTH,
                         height=FIELD_HEIGHT, scrollregion=(0, 0, FIELD_WIDTH, FIELD_HEIGHT))
        self.square_width = FIELD_WIDTH // COL_NUMBER
        self.square_height = FIELD_HEIGHT // ROW_NUMBER
        min_value = min(self.square_width, self.square_height)
        self.IMAGES = {tag: tk.PhotoImage(file=pict) for tag, pict in ICONS.items()}
        for key, value in self.IMAGES.items():
            image_width = value.width()
            self.IMAGES[key] = value.zoom(min_value // image_width or image_width // min_value)
        for i in range(1, ROW_NUMBER):
            current_y = self.square_height * i
            self.create_line(0, current_y, FIELD_WIDTH, current_y)
        for i in range(1, COL_NUMBER):
            current_x = self.square_width * i
            self.create_line(current_x, 0, current_x, FIELD_HEIGHT)

    def draw_image(self, x, y, race, tag):
        self.create_image((x + 0.5)*self.square_width, (y + 0.15)*self.square_height,
                          anchor=tk.NE, image=self.IMAGES[race], tag=tag)

    def move_top(self, tag):
        self.move(tag, 0, -self.square_height)

    def move_bottom(self, tag):
        self.move(tag, 0, self.square_height)

    def move_left(self, tag):
        self.move(tag, -self.square_width, 0)

    def move_right(self, tag):
        self.move(tag, self.square_width, 0)

    def delete_image(self, tag):
        self.delete(tag)
