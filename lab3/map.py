from ctypes import pointer
from math import floor
from turtle import width
import pygame

import math
import random
import time as tm
# from tqdm import tqdm
# from matplotlib import pyplot as plt



pygame.init()


col1 = "#E58C8A"
col2 = "#EEC0C6"

screen_width = 1090
screen_height = 505

_colony_size = 20
_steps = 50
_alpha = 1.0
_beta = 3.0
_rho = 0.1

bDIST = 100

WIDTH = 1090
HEIGHT = 507
cords = [(50.064523, 19.923654, "A0"),(50.065594, 19.921481, "Biblioteka"),(50.065821, 19.919346, "B1"),(50.066209, 19.921974, "C1"),(50.065685, 19.916957, "B8"),(50.06820297187411, 19.912773129000392, "D17"),(50.06746968697298, 19.914709024695757, "AMSO"),(50.067949564906606, 19.9080617470033, "Klub Studio"),(50.067535649739476, 19.90712102934611, "DS Kapitol"),(50.06747721436826, 19.90488303171917, "DS Stokrotka"),(50.06907690434182, 19.904403365047347, "DS Olimp"),(50.06917429333923, 19.90916764474132, "Cyfronet"),(50.06650089354261, 19.91091252427056, "D 10"),(50.06544779742544, 19.918577110902483, "URSS"), (50.065621, 19.915501, "DS Alfa"), (50.066989631130866, 19.91518774527342, "D5"), (50.06963635391785, 19.90580106554046, "Awiteks"),( 50.06731522168638, 19.917582940198812, "Lokomotywa"), (50.06433711282498, 19.92214218154198, "A1"),(50.067181675679365, 19.916417976399195, "B5"), (50.068718528830075, 19.90615498786142, "Grilownia"), (50.06731299353238, 19.91225734989374, "D11"), (50.067984778372036, 19.91051161859226, "Makarun"), (50.06878871984652, 19.91400359433865, "Kawiory"), (50.06679907434517, 19.92053796651356, "C5"), (50.06474315570295, 19.912085114089336, "Stadion"),(50.06623185805964, 19.911867057556606, "AKŻ")]

win = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("TSP with Ant Algorithm Solver")

bg = pygame.image.load('img/mapa.png')

#corners
c = [(50.070448, 19.903960, "lewy górny"), (50.067215, 19.902664, "lewy dolny"),(50.063575, 19.923404, "prawy dolny"),(50.066742, 19.924608, "prawy górny")]


class SolveTSPUsingACO:
    class Edge:
        def __init__(self, a, b, weight, initial_pheromone):
            self.a = a
            self.b = b
            if weight == 0:
                weight = 1e-10
            self.weight = weight
            self.pheromone = initial_pheromone

    class Ant:
        def __init__(self, alpha, beta, num_nodes, edges):
            self.alpha = alpha
            self.beta = beta
            self.num_nodes = num_nodes
            self.edges = edges
            self.tour = None
            self.distance = 0.0

        def _select_node(self):
            roulette_wheel = 0.0
            unvisited_nodes = [node for node in range(self.num_nodes) if node not in self.tour]
            heuristic_total = 0.0
            for unvisited_node in unvisited_nodes:
                heuristic_total += self.edges[self.tour[-1]][unvisited_node].weight
            for unvisited_node in unvisited_nodes:
                roulette_wheel += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * \
                                  pow((heuristic_total / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)
            random_value = random.uniform(0.0, roulette_wheel)
            wheel_position = 0.0
            for unvisited_node in unvisited_nodes:
                wheel_position += pow(self.edges[self.tour[-1]][unvisited_node].pheromone, self.alpha) * \
                                  pow((heuristic_total / self.edges[self.tour[-1]][unvisited_node].weight), self.beta)
                if wheel_position >= random_value:
                    return unvisited_node

        def find_tour(self):
            self.tour = [random.randint(0, self.num_nodes - 1)]
            while len(self.tour) < self.num_nodes:
                self.tour.append(self._select_node())
            return self.tour

        def get_distance(self):
            self.distance = 0.0
            for i in range(self.num_nodes):
                self.distance += self.edges[self.tour[i]][self.tour[(i + 1) % self.num_nodes]].weight
            return self.distance

    def __init__(self, mode='ACS', colony_size=10, elitist_weight=1.0, min_scaling_factor=0.001, alpha=1.0, beta=3.0,
                 rho=0.1, pheromone_deposit_weight=1.0, initial_pheromone=1.0, steps=100, nodes=None, labels=None):
        self.mode = mode
        self.colony_size = colony_size
        self.elitist_weight = elitist_weight
        self.min_scaling_factor = min_scaling_factor
        self.rho = rho
        self.pheromone_deposit_weight = pheromone_deposit_weight
        self.steps = steps
        self.num_nodes = len(nodes)
        self.nodes = nodes
        if labels is not None:
            self.labels = labels
        else:
            self.labels = range(1, self.num_nodes + 1)
        self.edges = [[None] * self.num_nodes for _ in range(self.num_nodes)]
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                self.edges[i][j] = self.edges[j][i] = self.Edge(i, j, math.sqrt(
                    pow(self.nodes[i][0] - self.nodes[j][0], 2.0) + pow(self.nodes[i][1] - self.nodes[j][1], 2.0)),
                                                                initial_pheromone)
        self.ants = [self.Ant(alpha, beta, self.num_nodes, self.edges) for _ in range(self.colony_size)]
        self.global_best_tour = None
        self.global_best_distance = float("inf")

    def _add_pheromone(self, tour, distance, weight=1.0):
        pheromone_to_add = self.pheromone_deposit_weight / distance
        for i in range(self.num_nodes):
            self.edges[tour[i]][tour[(i + 1) % self.num_nodes]].pheromone += weight * pheromone_to_add

    def _acs(self):
        for step in range(self.steps):
            for ant in self.ants:
                # Amout of pheromone increment is constant.
                self._add_pheromone(ant.find_tour(), ant.get_distance())
                if ant.distance < self.global_best_distance:
                    self.global_best_tour = ant.tour
                    self.global_best_distance = ant.distance
                    redraw_game_window(self.global_best_tour, self.global_best_distance)
                    clock.tick(60)
            for i in range(self.num_nodes):
                for j in range(i + 1, self.num_nodes):
                    self.edges[i][j].pheromone *= (1.0 - self.rho)

    def run(self):
        start = tm.time()
        if self.mode == 'ACS':
            self._acs()
        runtime = tm.time() - start
        return runtime, self.global_best_distance


def cordsReal2Anim(p):
    cor = [
            (50.070326, 19.903128), 
            (50.063801, 19.924061)]
    delta = (cor[0][0] - cor[1][0], cor[0][1] - cor[1][1])
    point = (p[0] - cor[0][0], p[1] - cor[0][1])
    ratio = ( - point[0] / delta[0], - point[1] / delta[1])
    return WIDTH * ratio[1], HEIGHT * ratio[0]


def sign(num):
    if num > 0:
        return 1
    if num == 0:
        return 0
    return -1

clock = pygame.time.Clock()


def redraw_game_window(tour = None, dist = None):
    global bDIST
    win.blit(bg, (0,0))
    font = pygame.font.Font('freesansbold.ttf', 14)

    if tour is not None:
        for i in range(0, len(tour)):
            pygame.draw.line(win, col1, cordsReal2Anim(cords[tour[i]]), cordsReal2Anim(cords[tour[(i+1)% len(tour)]]), 5)
    

    for pp in cords:
        x, y = cordsReal2Anim((pp))
        pygame.draw.circle(win, col1, (x, y), 13)
        text = font.render(pp[2], True, "#041B15", "#4CE0D2")
        textRect = text.get_rect()
        textRect.center = (x, y)
        win.blit(text, textRect)

    if tour is not None:
        km_dist = round(111*dist, 3)
        font = pygame.font.Font('freesansbold.ttf', 34)
        text = font.render(str(km_dist) + "km", True, "#041B15", "#4CE0D2")
        textRect = text.get_rect()
        textRect.center = (900, 50)
        win.blit(text, textRect)
        if km_dist < bDIST:
            print(km_dist)
            bDIST = km_dist

    if run_algo:
        font = pygame.font.Font('freesansbold.ttf', 34)
        text = font.render("Running", True, "#041B15", "#4CE0D2")
        textRect = text.get_rect()
        textRect.center = (80, 20)
        win.blit(text, textRect)

    pygame.display.update()
run = True
frame = 0

run_algo = False
win.blit(bg, (0,0))
redraw_game_window()
pygame.display.update()


while run:
    clock.tick(60)
    frame += 1
    if run_algo:
        

        acs = SolveTSPUsingACO(mode='ACS', colony_size=_colony_size, steps=_steps, nodes=cords, beta=_beta, alpha=_alpha, rho=_rho)
        time, dist = acs.run()
        run_algo = False
        
        font = pygame.font.Font('freesansbold.ttf', 34)
        text = font.render("Finished", True, "#041B15", "#4CE0D2")
        textRect = text.get_rect()
        textRect.center = (80, 20)
        win.blit(text, textRect)

        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        run_algo = not run_algo
