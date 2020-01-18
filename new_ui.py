import tkinter as tk
from time import sleep
from queue import Queue, Empty
from threading import Thread
from models import Cockroach, Snowflake, Washcloth
from random import randint, choice


FIELD_WIDTH = 70
FIELD_HEIGHT = 50
current_step = 0
game_play = False


class FrontWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("960x540+300+150")
        self.root.minsize(700, 300)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.toolbar = tk.Frame(self.root, highlightthickness=1, highlightbackground='black', width=300, height=300)
        self.toolbar.grid(row=0, column=3, sticky='ns', padx=(10, 0), pady=0)
        self.field = tk.Canvas(self.root, highlightthickness=1, highlightbackground='black',
                               bg='#004d99', relief='ridge', scrollregion=(0, 0, 1550, 900))
        self.field.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nswe', padx=(0, 10), pady=(0, 10))
        self.buttonbar = tk.Frame(self.root, highlightbackground='black', width=200, height=70, highlightthickness=1)
        self.buttonbar.grid(row=3, column=0, columnspan=2, rowspan=1, sticky='we', padx=(0, 10), pady=(10, 0))
        self.buttonbar.grid_rowconfigure(0, weight=1)
        self.buttonbar.grid_columnconfigure(0, weight=30)
        self.buttonbar.grid_columnconfigure(1, weight=1)
        self.buttonbar.grid_columnconfigure(2, weight=1)
        self.buttons = [
            tk.Button(self.buttonbar, text='Play', command=self.play, bg='#8beb77', activebackground='#77eb8b',
                      activeforeground='white', width=10).grid(row=0, column=5, pady=(10, 3), padx=(3, 10), sticky='we'),
            tk.Button(self.buttonbar, text='Pause', command=self.pause, bg='#e66e55', activebackground='#e68c55',
                      activeforeground='white', width=10).grid(row=1, column=5, pady=(3, 10), padx=(3, 10), sticky='we')
        ]
        self.step_var = tk.StringVar()
        self.step_var.set(f"Step number {current_step}")
        self.labels = [tk.Label(self.buttonbar, textvariable=self.step_var).grid(row=1, column=4, pady=(3, 10),
                                                                                 padx=(10, 3), sticky='we')]
        self.state = True
        self.squares = []
        for x in range(FIELD_HEIGHT):  # vertical
            self.squares.append([])
            for y in range(FIELD_WIDTH):  # horizontal
                self.squares[x].append(self.field.create_rectangle(y * 1550 // FIELD_WIDTH, x * 900 // FIELD_HEIGHT,
                                      (y+1) * 1550 // FIELD_WIDTH, (x+1) * 900 // FIELD_HEIGHT))
        xbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        ybar = tk.Scrollbar(self.root)
        ybar.grid(row=0, column=2, rowspan=3, sticky='ns')
        xbar.grid(row=2, column=0, columnspan=2, sticky='we')
        self.field.configure(xscrollcommand=xbar.set, yscrollcommand=ybar.set)
        xbar.config(command=self.field.xview)
        ybar.config(command=self.field.yview)
        self.root.attributes("-fullscreen", self.state)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        self.root.bind("<space>", self.change_run)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)

    # def play(self):
    #     global game_play, current_generation, current_step
    #     game_play = True
    #     print("cold", len(cold))
    #     print("warm", len(warm))
    #     if game_play and len(cold) > 0 and len(warm):
    #         for i in range(generation_steps):
    #             do_step()
    #             current_step = i
    #             print("generation ", current_generation, "step ", current_step)
    #             self.refresh()
    #         do_reproduction()
    #         sleep(1)
    #         print("cold", len(cold))
    #         print("warm", len(warm))
    #         current_generation += 1
    #         self.refresh()
    #     game_play = True
    #     self.buttons[0].config(state=tk.DISABLED)
    #     self.buttons[1].config(state=tk.NORMAL)

    def play(self):
        global game_play
        game_play = True
        # self.buttons[1].config(state=tk.DISABLED)
        # self.buttons[0].config(state=tk.NORMAL)

    def pause(self):
        global game_play
        game_play = False
        # self.buttons[1].config(state=tk.DISABLED)
        # self.buttons[0].config(state=tk.NORMAL)

    def change_run(self):
        global game_play
        game_play = not game_play

    # def refresh(self):
    #     for i in range(FIELD_HEIGHT):
    #         for j in range(FIELD_WIDTH):
    #             self.field.itemconfig(self.squares[i][j], fill=cells[i][j].color_by_view_mode(current_view_mode))
    #     self.generation_var.set(f"Generation number {current_generation}")
    #     self.step_var.set(f"Step number {current_step}")

    def init_logic(self):
        self.map = [['-' for j in range(0, int(self.scene.sceneRect().height()), self.sqr_width)]
                    for i in range(0, int(self.scene.sceneRect().width()), self.sqr_width)]
        self.sqr_view = 4
        self.creatures = []
        self.add_creature('Cockroach', 8, 5, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 9, 5, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 7, 6, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 8, 6, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 9, 6, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 7, 7, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 8, 7, MainWindow.gen_features('Cockroach'))
        self.add_creature('Snowflake', 42, 10, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 43, 10, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 42, 11, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 43, 11, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 44, 11, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 43, 12, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 44, 12, MainWindow.gen_features('Snowflake'))
        self.add_creature('Washcloth', 25, 19, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 24, 20, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 25, 20, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 26, 20, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 24, 21, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 25, 21, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 26, 21, MainWindow.gen_features('Washcloth'))
        self.gen_water()
        self.game = True
        self.start()

    def del_creature(self, creature):
        self.scene.remove(creature.item)
        self.map[creature.x][creature.y] = '-'
        self.creatures.remove(creature)

    def shuffle(self):
        def swap(creatures, i, j):
            creatures[i], creatures[j] = creatures[j], creatures[i]
        for _ in range(len(self.creatures) // 3):
            swap(self.creatures, randint(0, len(self.creatures) - 1), randint(0, len(self.creatures) - 1))

    def start(self):
        while self.game:
            self.shuffle()
            for cr in self.creatures:
                cr.turn()
            sleep(3)

    def add_creature(self, type, x, y, gene, gen_number=1):
        if type == 'Cockroach':
            obj = Cockroach(x, y, gene, gen_number, self)
        elif type == 'Snowflake':
            obj = Snowflake(x, y, gene, gen_number, self)
        else:
            obj = Washcloth(x, y, gene, gen_number, self)
        if self.map[x][y] is not '-':
            del obj
        else:
            self.map[x][y] = obj
            self.creatures.append(obj)
            self.scene.addItem(obj.item)

    def apocalepse(self):
        for _ in range(len(self.creatures)//2):
            self.del_creature(choice(self.creatures))

    @staticmethod
    def gen_features(type):
        gene = {"attack": {"-x": randint(8, 12) * 10, "+x": randint(8, 12) * 10,
                           "+y": randint(8, 12) * 10, "-y": randint(8, 12) * 10},
                "defense": {"-x": randint(0, 4) * 10, "+x": randint(0, 4) * 10,
                            "+y": randint(0, 4) * 10, "-y": randint(0, 4) * 10},
                "capacity": {"hp": randint(7, 14) * 100, "water": randint(7, 14) * 100}}
        if type == 'Cockroach':
            gene["capacity"]["vitamin"] = randint(7, 14) * 100
            gene["capacity"]["plant"] = randint(7, 14) * 100
        elif type == 'Snowflake':
            gene["capacity"]["meat"] = randint(7, 14) * 100
            gene["capacity"]["plant"] = randint(7, 14) * 100
        else:
            gene["capacity"]["vitamin"] = randint(7, 14) * 100
            gene["capacity"]["meat"] = randint(7, 14) * 100
        return gene

    def gen_water(self):
        for _ in range(30):
            i = randint(0, len(self.map) - 1)
            j = randint(0, len(self.map[i]) - 1)
            if self.map[i][j] == '-':
                self.map[i][j] = 'w'
                number = randint(1, 3)
                item = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(r"..\pict\water{}.png".format(number)))
                item.setOffset(i * self.sqr_width, j * self.sqr_width)
                self.scene.addItem(item)


class ThreadClient:
    def __init__(self, root):
        self.root = root
        self.queue = Queue()
        self.gui = FrontWindow(root)
        self.thread = Thread(target=self.start_game)
        self.thread.start()
        self.periodicCall()

    def start_game(self):
        self.queue.put(True)
        sleep(1)

    def periodicCall(self):
        while self.queue.qsize():
            try:
                self.queue.get()
                self.gui.refresh()
            except Empty:
                pass
        self.root.after(100, self.periodicCall)


if __name__ == '__main__':
    root = tk.Tk()
    client = ThreadClient(root)
    root.mainloop()
