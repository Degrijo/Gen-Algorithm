import tkinter as tk


from constants import ROW_NUMBER, COL_NUMBER


class View:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("960x540+300+150")
        self.root.minsize(700, 300)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        toolbar = tk.Frame(self.root, highlightthickness=1, highlightbackground='black', width=300)
        toolbar.grid(row=0, column=1, sticky='ns', padx=(0, 10), pady=(10, 10))
        self.field = tk.Canvas(self.root, highlightthickness=1, highlightbackground='black',
                               bg='#004d99', relief='ridge', width=700, height=400)  # scrollregion=(0, 0, 1550, 900)
        self.field.grid(row=0, column=0, sticky='nswe', padx=(10, 10), pady=(10, 10))
        field_height = int(self.field['height'])
        field_width = int(self.field['width'])
        square_height = field_height // ROW_NUMBER
        for i in range(1, ROW_NUMBER):
            current_y = square_height * i
            self.field.create_line(0, current_y, field_width, current_y, width=10)
        square_width = field_width // COL_NUMBER
        for i in range(1, COL_NUMBER):
            current_x = square_width * i
            self.field.create_line(current_x, 0, current_x, field_height)
        print('square width', square_width, 'square height', square_height)
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

    def del_image(self):
        self.field

    def draw_image(self, x, y, pict):
        self.field.itemconfig(self.field.create_rectangle(), fill=pict)

    def display(self):
        self.root.mainloop()
