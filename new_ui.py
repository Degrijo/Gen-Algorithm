import tkinter as tk
from new_models import Cell, Cockroach, Snowflake, Washcloth
from random import choice, randint
from threading import Thread
from time import sleep
import logging
from json import load, dump
from datetime import datetime


FIELD_WIDTH = 70
FIELD_HEIGHT = 50
FIELD_VIEW = 4
SPECIES = (Cockroach, Snowflake, Washcloth)
SPECIES_SIZE = 5
STEP_PAUSE = 1
STEPS_FOR_SAVING = 50

current_step = 0
game_play = False
creatures = []
chart = [[Cell() for j in range(FIELD_HEIGHT)] for i in range(FIELD_WIDTH)]
for i in range(FIELD_WIDTH):
    for j in range(FIELD_HEIGHT):
        chart[i][j].set_neighbors(chart[i][j] if not j else None, chart[i][j] if i != FIELD_WIDTH - 1 else None,
                                  chart[i][j] if j != FIELD_HEIGHT - 1 else None, chart[i][j] if not i else None)


def ui(root):
    root.geometry("960x540+300+150")
    root.minsize(700, 300)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    toolbar = tk.Frame(root, highlightthickness=1, highlightbackground='black', width=300, height=300)
    toolbar.grid(row=0, column=3, sticky='ns', padx=(10, 0), pady=0)
    field = tk.Canvas(root, highlightthickness=1, highlightbackground='black',
                           bg='#004d99', relief='ridge', scrollregion=(0, 0, 1550, 900))
    field.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nswe', padx=(0, 10), pady=(0, 10))
    buttonbar = tk.Frame(root, highlightbackground='black', width=200, height=70, highlightthickness=1)
    buttonbar.grid(row=3, column=0, columnspan=2, rowspan=1, sticky='we', padx=(0, 10), pady=(10, 0))
    buttonbar.grid_rowconfigure(0, weight=1)
    buttonbar.grid_columnconfigure(0, weight=30)
    buttonbar.grid_columnconfigure(1, weight=1)
    buttonbar.grid_columnconfigure(2, weight=1)
    buttons = [
        tk.Button(buttonbar, text='Play', bg='#8beb77', activebackground='#77eb8b',
                  activeforeground='white', width=10).grid(row=0, column=5, pady=(10, 3), padx=(3, 10), sticky='we'),
        tk.Button(buttonbar, text='Pause', bg='#e66e55', activebackground='#e68c55',
                  activeforeground='white', width=10).grid(row=1, column=5, pady=(3, 10), padx=(3, 10), sticky='we')
    ]
    step_var = tk.StringVar()
    step_var.set(f"Step number {current_step}")
    labels = [tk.Label(buttonbar, textvariable=step_var).grid(row=1, column=4, pady=(3, 10),
                                                                             padx=(10, 3), sticky='we')]
    state = True
    for x in range(FIELD_WIDTH):
        for y in range(FIELD_HEIGHT):
            chart[x][y].canvas_item = field.create_rectangle(x * 1550 // FIELD_WIDTH, y * 900 // FIELD_HEIGHT,
                                                 (x+1) * 1550 // FIELD_WIDTH, (y+1) * 900 // FIELD_HEIGHT)
    xbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    ybar = tk.Scrollbar(root)
    ybar.grid(row=0, column=2, rowspan=3, sticky='ns')
    xbar.grid(row=2, column=0, columnspan=2, sticky='we')
    field.configure(xscrollcommand=xbar.set, yscrollcommand=ybar.set)
    xbar.config(command=field.xview)
    ybar.config(command=field.yview)
    root.attributes("-fullscreen", state)

    def toggle_fullscreen(e):
        nonlocal state, root
        state = not state
        root.attributes("-fullscreen", state)

    def end_fullscreen(e):
        nonlocal state, root
        state = False
        root.attributes("-fullscreen", False)

    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", end_fullscreen)
    return field, step_var


def generate_creatures():
    global creatures, chart
    for species in SPECIES:
        for number in range(SPECIES_SIZE):
            x, y = randint(0, FIELD_WIDTH - 1), randint(0, FIELD_HEIGHT - 1)
            while True:
                if chart[x][y].is_empty:
                    creature = species(x, y)
                    creatures.append(creature)
                    chart[x][y].creatures.append(creature)
                    break
                x, y = randint(0, FIELD_WIDTH - 1), randint(0, FIELD_HEIGHT)
    update_chart()


def shuffle_creatures():
    global creatures

    def swap(items, i, j):
        items[i], items[j] = items[j], items[i]
    for _ in range(len(creatures) // 3):
        swap(creatures, randint(0, len(creatures) - 1), randint(0, len(creatures) - 1))


def update_chart():
    global field, step_var
    for i in range(FIELD_WIDTH):
        for j in range(FIELD_HEIGHT):
            field.itemconfig(chart[i][j].canvas_item, fill=chart[i][j].pict)
    step_var.set(f"Step number {current_step}")


def dump_sys():
    with open(f"backup{datetime.now().strftime('%d-%m-%Y_%H-%M')}.txt", 'w') as file:
        dump({
                 "FIELD_WIDTH": FIELD_WIDTH, "FIELD_HEIGHT": FIELD_HEIGHT,
                 "FIELD_VIEW": FIELD_VIEW, "SPECIES": SPECIES,
                 "SPECIES_SIZE": SPECIES_SIZE, "current_step": current_step,
                 "chart": [chart[i][j].to_json for i in range(FIELD_WIDTH) for j in range(FIELD_HEIGHT)]
              }, file, sort_keys=True, separators=(',', ':'), indent=4)


def step():
    global current_step
    while 1 > 0:
        shuffle_creatures()
        for creature in creatures:
            creature.turn()
        current_step += 1
        # update_chart()
        if not current_step % STEPS_FOR_SAVING:
            dump_sys()
        sleep(STEP_PAUSE)


if __name__ == '__main__':
    root = tk.Tk()
    field, step_var = ui(root)
    generate_creatures()
    game_thread = Thread(target=step)
    game_thread.start()
    root.mainloop()
