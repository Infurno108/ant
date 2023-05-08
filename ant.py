import os as os
import math as math
import random as random
import time as time
grid = 5
# y first x second


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class agent():
    def __init__(self, type, location):
        self.type = type
        self.location = location

    def move(self):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        self.location = [max(min(self.location[0] + y, grid), 0),
                         max(min(self.location[1] + x, grid), 0)]


def agentPrint():
    rows, cols = (grid, grid)
    map = [["O"]*rows]*cols
    for i in range(0, len(agents)):
        map[agents[i].location[0]][agents[i].location[1]] = "X"
    for row in map:
        print(row)


def agentMove():
    for i in range(0, len(agents)):
        agents[i].move()


ant = agent("ant", [0, 0])

agents = [ant]

while (True):
    agentPrint()
    agentMove()
    print()
    time.sleep(1)
