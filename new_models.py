from random import choice
from abc import ABC
from tkinter import PhotoImage
from random import randint


class Creature(ABC):  # можно сделать общую память для каждой рассы, observe возвращает словарь
    def __init__(self, x, y, gene, gen_number, parent):  # можно добавить имя и выводить его сверху
        self.x = x  # можно сделать возможность передавать ресурсы между однорассниками с процентом
        self.y = y
        self.sqr_width = parent.sqr_width
        self.sqr_view = parent.sqr_view
        self.direction = choice(['+x', '-x', '+y', '-y'])
        self.parent = parent
        self.gene = gene
        self.gen_number = gen_number
        self.map = parent.map
        self.resources = {res: int(gene["capacity"][res] * 0.8) for res in gene["capacity"] if res != "hp"}
        self.hp = gene["capacity"]["hp"]
        self.memory = {res: [] for res in self.resources}
        self.friends = []
        self.turn_number = 0
        self.mature = False
        self.plan = tuple()

    def turn(self):
        self.observe()  # наблюдение
        self.make_decision()  # принятие решение
        self.check_logistic()  # прокладка пути и его исполнение
        self.turn_finish()  # старение, проверка на смерть

    def observe(self):
        gap_x = [0, len(self.map)]
        gap_y = [0, len(self.map[0])]
        for i in self.memory:
            if i != 'water':
                self.memory[i].clear()
        self.friends.clear()
        if self.sqr_view < self.x:
            gap_x[0] = self.x - self.sqr_view
        if self.x + self.sqr_view < len(self.map) - 1:
            gap_x[1] = self.x + self.sqr_view + 1
        if self.sqr_view < self.y:
            gap_y[0] = self.y - self.sqr_view
        if self.y < len(self.map[0]) - 1 - self.sqr_view:
            gap_y[1] = self.y + self.sqr_view + 1
        for i in range(gap_x[0], gap_x[1]):
            for j in range(gap_y[0], gap_y[1]):
                if self.map[i][j] == '-':
                    continue
                elif self.map[i][j] == 'w' and (i, j) not in self.memory['water']:
                    self.memory['water'].append((i, j))
                elif type(self.map[i][j]) is type(self):
                    if self.map[i][j] is not self:
                        self.friends.append(self.map[i][j])
                elif type(self.map[i][j]) is Cockroach:
                    self.memory['meat'].append((i, j))
                elif type(self.map[i][j]) is Snowflake:
                    self.memory['vitamin'].append((i, j))
                elif type(self.map[i][j]) is Washcloth:
                    self.memory['plant'].append((i, j))

    def make_decision(self):
        first_need = []
        for key in self.resources:
            if self.resources[key] // self.gene["capacity"][key] <= 0.3:
                first_need.append(key)
        if not first_need:
            self.mature = True
            if self.friends:
                for fr in self.friends:
                    if fr.mature:
                        self.plan = "reproduction", (fr.x, fr.y)
                        print(1, self.plan)
            elif min(self.resources.values()) <= 150:
                key = list(self.resources.keys())[list(self.resources.values()).index(min(self.resources.values()))]
                if self.memory[key]:
                    if key is 'water':
                        self.plan = "drinking", self.min_path_to_res(key)
                        print(2, self.plan)
                    else:
                        self.plan = "eating", self.min_path_to_res(key)
                        print(3, self.plan)
        else:
            self.mature = False
            second_need = []
            for res in first_need:
                if res is not "water":
                    if self.memory[res]:
                        second_need.append(res)
            if second_need:
                self.plan = "eating", self.min_path_to_res(second_need[0])
                print(4, self.plan)
            else:
                if "water" in first_need:
                    self.plan = "drinking", self.min_path_to_res("water")
                    print(5, self.plan)
                else:
                    self.plan = "waiting", (-1, -1)
                    print(6, self.plan)

    def min_path_to_res(self, res):
        if not self.memory[res]:
            return
        elif len(self.memory[res]) == 1:
            return self.memory[res]
        min = -1
        for feach in self.memory[res]:
            if min == -1:
                min = feach
            else:
                print('min_path')
                if Creature.distance(feach, (self.x, self.y)) < Creature.distance(min, (self.x, self.y)):
                    min = feach
        return min

    @staticmethod
    def distance(a, b):
        print(a, b)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def check_logistic(self):
        if self.plan[0] is not "waiting":  # при waiting потрулирование территории
            print('check_logic')
            if Creature.distance((self.x, self.y), self.plan[1]) is 1:
                if self.plan[0] is "eating":
                    self.eat(self.plan[1])
                elif self.plan[0] is "drinking":
                    self.drink(self.plan[1])
                elif self.plan[0] is "reproduction":
                    self.reproduce(self.plan[1])
            else:
                # if self.plan[0] is  not "drinking":
                # if abs(self.x - self.plan[1][0]) == self.sqr_view and  or abs(self.y - self.plan[1][1]) == self.sqr_view:
                # else:
                sides = ['+x', '-x', '+y', '-y']
                if self.x == len(self.map) - 1 or self.map[self.x + 1][self.y] is not '-':
                    sides.remove('+x')
                elif self.x == 0 or self.map[self.x - 1][self.y] is not '-':
                    sides.remove('-x')
                if self.y == len(self.map[0]) - 1 or self.map[self.x][self.y + 1] != '-':
                    sides.remove('-y')
                elif self.y == 0 or self.map[self.x][self.y - 1] != '-':
                    sides.remove('+y')
                if sides:
                    if self.x - self.plan[1][0] is not 0:
                        if self.x > self.plan[1][0] and '-x' in sides:
                            self.direction = '-x'
                            self.to_step()
                            return
                        elif self.x < self.plan[1][0] and '+x' in sides:
                            self.direction = '+x'
                            self.to_step()
                            return
                    if self.y - self.plan[1][1] is not 0:
                        if self.y > self.plan[1][1] and '+y' in sides:
                            self.direction = '+y'
                            self.to_step()
                            return
                        elif self.y > self.plan[1][1] and '-y' in sides:
                            self.direction = '-y'
                            self.to_step()
                            return
                    self.direction = choice(sides)
                    self.to_step()  # может зациклиться и ходить из одной клетки в другую, решить эту проблему
        return

    def to_step(self):
        self.rotate()
        self.map[self.x][self.y] = '-'
        if self.direction == '+x':
            self.x += self.sqr_width
        elif self.direction == '-x':
            self.x -= self.sqr_width
        elif self.direction == '+y':
            self.y -= self.sqr_width
        else:
            self.y += self.sqr_width
        self.map[self.x][self.y] = self
        self.item.setPos(self.x, self.y)

    def rotate(self):
        if self.direction == '+x':
            self.item.setRotation(90)
        elif self.direction == '-x':
            self.item.setRotation(-90)
        elif self.direction == '+y':
            self.item.setRotation(180)
        else:
            self.item.setRotation(0)

    def rotate_to(self, matter):
        if matter[0] > self.x:
            self.direction = '+x'
        elif matter[0] < self.x:
            self.direction = '-x'
        elif matter[1] < self.y:
            self.direction = '+y'
        else:
            self.direction = '-y'
        self.rotate()

    def eat(self, matter):
        self.rotate_to(matter)
        enemy = self.map[matter[0]][1]
        if self.direction[0] is '+':
            enemy_direction = '-' + self.direction[1]
        else:
            enemy_direction = '+' + self.direction[1]
        damage = self.gene["attack"][self.direction] - enemy.gene["defense"][enemy_direction]
        if type(enemy) is Cockroach:
            self.resources["meat"] += damage
            if self.resources["meat"] > self.gene["capacity"]["meat"]:
                self.resources["meat"] = self.gene["capacity"]["meat"]
        elif type(enemy) is Snowflake:
            self.resources["vitamin"] += damage
            if self.resources["vitamin"] > self.gene["capacity"]["vitamin"]:
                self.resources["vitamin"] = self.gene["capacity"]["vitamin"]
        else:
            self.resources["plant"] += damage
            if self.resources["plant"] > self.gene["capacity"]["plant"]:
                self.resources["plant"] = self.gene["capacity"]["plant"]
        enemy.hp -= damage
        enemy.is_dead()

    def drink(self, matter):
        self.rotate_to(matter)
        self.resources["water"] += self.gene["attack"][self.direction]
        if self.resources["water"] > self.gene["capacity"]["water"]:
            self.resources["water"] = self.gene["capacity"]["water"]

    def reproduce(self, matter):
        self.rotate_to(matter)
        partner = self.map[matter[0]][matter[1]]
        partner.rotate_to((self.x, self.y))
        if type(self) is Cockroach:
            self.take_res('vitamin', 0.3 * self.gene['capacity']['vitamin'])
            self.take_res('plant', 0.3 * self.gene['capacity']['plant'])
        elif type(self) is Snowflake:
            self.take_res('plant', 0.3 * self.gene['capacity']['plant'])
            self.take_res('meat', 0.3 * self.gene['capacity']['meat'])
        else:
            self.take_res('vitamin', 0.3 * self.gene['capacity']['vitamin'])
            self.take_res('meat', 0.3 * self.gene['capacity']['meat'])
        self.take_res('water', 0.3 * self.gene['capacity']['water'])  # варики с большим значением и с рандомным
        gene = self.gene.copy()
        for key_i in gene:
            for key_j in gene[key_i]:  # мутации!
                if partner.gene[key_i][key_j] > gene[key_i][key_j]:
                    gene[key_i][key_j] = partner.gene[key_i][key_j]
        coor = ()
        for x in range(self.x - 1, self.x + 1):
            for y in range(self.y - 1, self.y + 1):
                if self.map[x][y] is '-':
                    coor = (x, y)
                    break
        self.parent.add_creature(str(type(self)), coor[0], coor[1], gene, self.gen_number + 1)

    def add_res(self, res, number):
        self.resources[res] += number
        if self.resources[res] > self.gene['capacity'][res]:
            self.resources = self.gene['capacity'][res]

    def take_res(self, res, number):
        self.resources[res] -= number
        if self.resources[res] < 0:
            self.resources = 0

    def turn_finish(self):
        for res in self.resources:
            if res is 0:
                self.hp -= 30
        self.turn_number += 1
        self.hp -= 2 * self.turn_number
        self.is_dead()

    def is_dead(self):
        if self.hp <= 0:
            self.parent.del_creature(self)

    def get_hero_inf(self):
        inf = ['  ', str(self.gen_number), " generation"]
        for key in ['attack', 'defense', 'capacity']:
            inf.append('\n'+key+'\n')
            counter = 0
            for value in self.gene[key]:
                if counter is 2:
                    counter = 0
                    inf.append('\n')
                inf.append(value + ' ' + str(self.gene[key][value])+', ')
                counter += 1
        inf[-1] = inf[-1][:-2]
        return ' '.join(inf)

    @property
    def to_json(self):
        return {"gene": self.gene, "gen_number": self.gen_number, "resources": self.resources, "hp": self.hp,
                "memory": self.memory, "friends": self.friends, "turn_number": self.turn_number, "mature": self.mature,
                "plan": self.plan}


# class Cockroach(Creature):
#     def __init__(self, x, y, gene, gen_number, parent):
#         super().__init__(x, y, gene, gen_number, parent)
#         self.pict = PhotoImage(file=r"..\pict\cockroach.png")
#
#
# class Snowflake(Creature):
#     def __init__(self, x, y, gene, gen_number, parent):
#         super().__init__(x, y, gene, gen_number, parent)
#         self.pict = PhotoImage(file=r"..\pict\snowflake.png")
#
#
# class Washcloth(Creature):
#     def __init__(self, x, y, gene, gen_number, parent):
#         super().__init__(x, y, gene, gen_number, parent)
#         self.pict = PhotoImage(file=r"..\pict\washcloth.png")


class Cell:
    def __init__(self):
        self.creatures = []
        self.up = self.right = self.down = self.left = None
        self.canvas_item = None
        self.water = 0

    def set_neighbors(self, up, right, down, left):
        self.up, self.right, self.down, self.left = up, right, down, left

    @property
    def is_empty(self):
        return True if not self.creatures else False

    @property
    def pict(self):
        if self.water:
            # return PhotoImage(file=rf"pict/water{randint(1, 3)}.png")
            return '#0000C8'
        if self.creatures:
            return self.creatures[0].pict

    @property
    def to_json(self):
        return {"water": self.water, "creatures": [obj.to_json for obj in self.creatures]}


class Cockroach:
    def __init__(self, x, y):
        self.pict = '#640000'

    def turn(self):
        print('cockroach step')


class Snowflake:
    def __init__(self, x, y):
        self.pict = '#9B38D9'

    def turn(self):
        print('snowflake step')


class Washcloth:
    def __init__(self, x, y):
        self.pict = "#DC3E3E"

    def turn(self):
        print('washcloth step')
