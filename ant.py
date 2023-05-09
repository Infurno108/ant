import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os as os
import math as math
import random as random
import time as time
import copy as copy
grid = 51  # 6 actually means like 5 by 5
# y first x second
map = [["0" for i in range(grid - 1)] for j in range(grid - 1)]


def clear():
    os.system('clear')


class agent():
    def __init__(self, name, location, color, handle, dna):
        self.name = name
        self.energy = 10
        self.location = location
        self.mapLocation = graphToMap(location)
        self.oldSpot = location
        self.color = color
        self.handle = handle
        self.children = []
        self.dna = dna
        self.rna = dna
        self.childCount = 0

    def express(self):
        # This is going to need to decide between moving, reproducing, eating, constructing. Then call that method. For now lets just use random.
        # this will later need to be based on NN
        # 1 = up, 2 = right, 3 = down, 0 = left
        # M = move, R = reproduce, E = eat, C = construct
        # 1L 2M 3L 2M

        if (len(self.rna) == 0):
            self.rna = self.dna
        codon = self.rna[:2]  # first two elements of RNA
        self.rna = self.rna[2:]  # removes first two elements of RNA
        direction = int(codon[0])

        # print("Command: " + str(codon[1]) + " direction: " +
        #      str(direction) + " Location: " + str(self.location) + " Codon: " + str(codon))
        if (codon[1] == "M"):
            self.move(direction)
        if (codon[1] == "L"):
            self.construct(direction)
        if (codon[1] == "R"):
            self.reproduce(direction)

    def reproduce(self, direction):
        global agents
        if (self.energy > 30):
            self.energy = self.energy - 30
            self.children.append(agent(self.name + "child" + str(self.childCount), self.location, self.color, plt.scatter(
                self.location[0]-.5, self.location[1] - .5, color=self.color), self.dna))
            self.childCount = self.childCount + 1
            self.children[-1].move(direction)
            agents.append(self.children[-1])

    def construct(self, direction):
        global leaf
        scout = copy.copy(self.location)
        if direction == 0:
            if self.location[0] == 1:
                scout[0] = grid - 1
            else:
                scout[0] -= 1
        elif direction == 1:
            if self.location[1] == grid - 1:
                scout[1] = 1
            else:
                scout[1] += 1
        elif direction == 2:
            if self.location[0] == grid - 1:
                scout[0] = 1
            else:
                scout[0] += 1
        elif direction == 3:
            if self.location[1] == 1:
                scout[1] = grid - 1
            else:
                scout[1] -= 1
        scoutTranslated = graphToMap(scout)
        if map[scoutTranslated[0]][scoutTranslated[1]] == "0":
            leafLocal = scout
            self.children.append(leaf(leafLocal, plt.scatter(
                leafLocal[0]-.5, leafLocal[1] - .5, color="darkgreen"), self))

    def move(self, direction):
        global map
        # direction: 0 = left, 1 = up, 2 = right, 3 = down
        self.energy = self.energy - .1
        scout = copy.copy(self.location)
        if direction == 0:
            if self.location[0] == 1:
                scout[0] = grid - 1
            else:
                scout[0] -= 1
        elif direction == 1:
            if self.location[1] == grid - 1:
                scout[1] = 1
            else:
                scout[1] += 1
        elif direction == 2:
            if self.location[0] == grid - 1:
                scout[0] = 1
            else:
                scout[0] += 1
        elif direction == 3:
            if self.location[1] == 1:
                scout[1] = grid - 1
            else:
                scout[1] -= 1
        scoutTranslated = graphToMap(scout)
        if map[scoutTranslated[0]][scoutTranslated[1]] == "0":
            self.location = scout
        
    def update(self):
        global map
        self.handle.remove()
        self.handle = plt.scatter(
            self.location[0]-.5, self.location[1]-.5, color=self.color)
        map[self.mapLocation[0]][self.mapLocation[1]] = "0"
        self.mapLocation = graphToMap(self.location)
        map[self.mapLocation[0]][self.mapLocation[1]] = "X"
        for child in self.children:
            child.update()


class leaf():
    def __init__(self, location, handle, parent):
        self.location = location
        self.mapLocation = graphToMap(location)
        self.color = "darkgreen"
        self.handle = handle
        self.parent = parent

    def update(self):
        global map
        self.parent.energy = self.parent.energy + .1
        map[self.mapLocation[0]][self.mapLocation[1]] = "L"

    
def mapPrint():
    for row in map:
        print(row)
    print()


def mapUpdate(fig):
    for agent in agents:
        agent.update()
        agent.express()


def graphToMap(location):  # locaiton 0 is x 1 is y
    return [(grid - 1) - location[1], location[0] - 1]


# Setting up the grid that the agents will move on
x = np.linspace(0, grid - 1)  # these two set up arrays full of just 1 - 4
y = np.linspace(0, grid - 1)
fig = plt.figure()  # figure variable for the animation
ax = plt.axes()  # axes variable
# sets the limits of the x axis, that way blocks are right
plt.xlim(0, grid - 1)
plt.ylim(0, grid - 1)
ax.set_yticklabels([])
ax.set_xticklabels([])  # these get rid of the numbers on the axes
# plt.axis('off')

plt.xticks(np.arange(0, grid, 1))
plt.yticks(np.arange(0, grid, 1))  # these set the lines to be only 1 step
plt.grid(True)  # grido

shallow = 3
deep = grid - 3

ant = agent("ant", [shallow, shallow], "red", plt.scatter(
    shallow - .5, shallow - .5, color="red"), "2M1L2M1M0R2M3M3M2M3L")  # declaration of agents 1L2M3L2M

# 2L1M3M2L
# will need to think of a less clunky way of doing this

# rat = agent("rat", [deep, deep], "blue", plt.scatter(
#    deep - .5, deep - .5, color="blue"))

# cat = agent("cat", [deep, shallow], "magenta", plt.scatter(
#    deep - .5, shallow - .5, color="magenta"))

# bat = agent("bat", [shallow, deep], "orange", plt.scatter(
#    shallow - .5, deep - .5, color="orange"))

# map init, temp

agents = [ant]

ani = animation.FuncAnimation(fig, mapUpdate, interval=1)

plt.show()
print("let me out")
# while (True):
#    agentMove()
#    mapUpdate()
#    mapPrint()
#    scatterUpdate()
#    print()
#    time.sleep(1)
