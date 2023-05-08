import os as os
import math as math
import random as random
x = 3
y = 3
# y first x second


class agent():
    def __init__(self, type, location):
        self.type = type
        self.location = location

    def move(self):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        self.location = [max(min(self.location[0] + y, 2), 0),
                         max(min(self.location[1] + x, 2), 0)]


def agentPrint():
    map = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(0, len(agents)):
        map[agents[i].location[0]][agents[i].location[1]] = 1
    for i in range(0, len(map)):
        print(map[i])


ant = agent("ant", [0, 0])

agents = [ant]

agentPrint()

ant.move()
print()

agentPrint()

while (True):
    mapPrint(map)
