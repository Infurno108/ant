import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os as os
import math as math
import random as random
import time as time
import copy as copy
import sys as sys
from matplotlib import style
grid = 101  # 6 actually means like 5 by 5
# y first x second
map = [["0" for i in range(grid - 1)] for j in range(grid - 1)]
antCount = 0
leafCount = 0
energy = 30
reproduceCost = 30
moveCost = 20
leafCost = 5

red = ["lightsalmon", "salmon", "darksalmon", "lightcoral",
       "indianred", "crimson", "firebrick", "darkred"]

blue = ["lightsteelblue", "powderblue", "lightblue", "skyblue", "lightskyblue", "deepskyblue", "dodgerblue",
        "cornflowerblue", "steelblue", "royalblue", "blue", "mediumblue", "darkblue", "navy", "midnightblue"]

purple = ["lavender", "thistle", "plum", "violet", "orchid", "fuchsia", "magenta", "mediumorchid",
          "mediumpurple", "blueviolet", "darkviolet", "darkorchid", "darkmagenta", "purple", "indigo"]

brown = ["cornsilk", "blanchedalmond", "bisque", "navajowhite", "wheat", "burlywood", "tan", "rosybrown",
         "sandybrown", "goldenrod", "darkgoldenrod", "peru", "chocolate", "saddlebrown", "sienna", "brown", "maroon"]


def colorPicker(color):
    if (color == "red"):
        return red[random.randint(0, len(red) - 1)]
    elif (color == "blue"):
        return blue[random.randint(0, len(blue) - 1)]
    elif (color == "purple"):
        return purple[random.randint(0, len(purple) - 1)]
    elif (color == "brown"):
        return brown[random.randint(0, len(brown) - 1)]


def clear():
    os.system('clear')


class agent():
    def __init__(self, location, color, handle, dna, root):
        global energy
        self.energy = 30
        self.location = location
        self.mapLocation = graphToMap(location)
        self.color = color
        self.root = root
        self.lives = 5
        self.handle = handle
        self.leaves = []
        self.dna = dna
        self.rna = dna

    def express(self):
        # This is going to need to decide between moving, reproducing, eating, constructing. Then call that method. For now lets just use random.
        # this will later need to be based on NN
        # 1 = up, 2 = right, 3 = down, 0 = left
        # M = move, R = reproduce, E = eat, C = construct
        # 1L 2M 3L 2M
        if (len(self.rna) < 2):
            self.rna = self.dna
        direction = int(self.rna[0])
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
            self.lives = 5
            if (self.rna[1] == "M"):
                self.move(scout)
            if (self.rna[1] == "L"):
                self.construct(scout)
            if (self.rna[1] == "R"):
                self.reproduce(scout)
        else:
            self.lives = self.lives - 1
        self.rna = self.rna[2:]

    def kill(self):
        global agents, antCount
        self.handle.remove()
        map[self.mapLocation[0]][self.mapLocation[1]] = "0"
        for leaf in self.leaves:
            leaf.handle.remove()
            map[leaf.mapLocation[0]][leaf.mapLocation[1]] = "0"
        agents.remove(self)
        antCount = antCount - 1

    def reproduce(self, scout):
        global antCount, reproduceCost, agents
        if (self.energy > reproduceCost):  # self.energy > reproduceCost
            antCount = antCount + 1
            mutation = mutate(self.dna, self.root)
            self.energy = self.energy - reproduceCost
            agents.append(agent(scout, mutation[1], plt.scatter(
                scout[0]-.5, scout[1] - .5, color=self.color), mutation[0], self.root))

    def construct(self, scout):
        global leaf, leafCost, leafCount
        if (self.energy > leafCost):
            leafCount = leafCount + 1
            self.energy - leafCost
            self.leaves.append(leaf(scout, plt.scatter(
                scout[0]-.5, scout[1] - .5, color="darkgreen"), self))

    def move(self, scout):
        global map, moveCost
        # direction: 0 = left, 1 = up, 2 = right, 3 = down
        if (self.energy > moveCost):
            self.energy = self.energy - moveCost
            self.location = scout

    def update(self):
        global map
        if (energy < 0 or self.lives < 0):
            self.kill()
        else:
            self.handle.remove()
            self.handle = plt.scatter(
                self.location[0]-.5, self.location[1]-.5, color=self.color)
            map[self.mapLocation[0]][self.mapLocation[1]] = "0"
            self.mapLocation = graphToMap(self.location)
            map[self.mapLocation[0]][self.mapLocation[1]] = "X"
            for leaf in self.leaves:
                leaf.update()


class leaf():
    def __init__(self, location, handle, parent):
        self.location = location
        self.mapLocation = graphToMap(location)
        self.color = "darkgreen"
        self.handle = handle
        self.parent = parent

    def update(self):
        global map
        self.parent.energy = self.parent.energy + 1
        map[self.mapLocation[0]][self.mapLocation[1]] = "L"


def mapPrint():
    for row in map:
        print(row)
    print(antCount)
    print()


def mapUpdate(fig):
    for agent in agents:
        agent.update()
        agent.express()


def graphToMap(location):  # locaiton 0 is x 1 is y
    return [(grid - 1) - location[1], location[0] - 1]


def randomCodon():
    return str(random.randint(0, 3)) + random.choice(["M", "L", "R"])


def randomDNA():
    bap = random.randint(1, 21)
    returnString = ""
    for i in range(0, bap):
        returnString = returnString + randomCodon()
    return returnString


def mutate(DNA, color):
    if (random.randint(0, 20) == 0):  # sucesstest
        # checking for the type of mutation #remind friedrich that my AI told me the types of dna mutations
        temp = random.randint(0, 3)
        location = random.randint(0, len(DNA) - 1)  # location of the mutation
        try:
            int(DNA[location])
        except:
            location = location - 1
        codon = randomCodon()
        if (temp == 0):  # substitution
            DNA = str(DNA[:location] + codon + DNA[location + 2:])
        elif (temp == 1):  # insertion
            DNA = str(DNA[:location] + codon + DNA[location:])
        elif (temp == 2):  # deletion
            DNA = str(DNA[:location] + DNA[location + 2:])
    return [DNA, colorPicker(color)]


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
plt.style.use('dark_background')
plt.xticks(np.arange(0, grid, 1))
plt.yticks(np.arange(0, grid, 1))  # these set the lines to be only 1 step
plt.grid(True)  # grido

shallow = 3
deep = grid - 3
half = int((grid - 1) / 2)
antDNA = randomDNA()
ant = agent([shallow, shallow], "red", plt.scatter(
    shallow - .5, shallow - .5, color="red"), antDNA, "red")  # declaration of agents 1L2M3L2M

# will need to think of a less clunky way of doing this
ratDNA = randomDNA()
rat = agent([deep, deep], "blue", plt.scatter(
    deep - .5, deep - .5, color="blue"), ratDNA, "blue")

catDNA = randomDNA()
cat = agent([deep, shallow], "magenta", plt.scatter(
    deep - .5, shallow - .5, color="magenta"), catDNA, "purple")

batDNA = randomDNA()
bat = agent([shallow, deep], "orange", plt.scatter(
    shallow - .5, deep - .5, color="orange"), batDNA, "brown")

antTwoDNA = randomDNA()
antTwo = agent([half, shallow], "red", plt.scatter(
    half - .5, shallow - .5, color="red"), antTwoDNA, "red")
ratTwoDNA = randomDNA()
ratTwo = agent([half, deep], "blue", plt.scatter(
    half - .5, deep - .5, color="blue"), ratTwoDNA, "blue")

catTwoDNA = randomDNA()
catTwo = agent([deep, half], "magenta", plt.scatter(
    deep - .5, half - .5, color="magenta"), catTwoDNA, "purple")

batTwoDNA = randomDNA()
batTwo = agent([shallow, half], "orange", plt.scatter(
    shallow - .5, half - .5, color="orange"), batTwoDNA, "brown")

print("Ant DNA: " + antDNA + "\nRat DNA: " + ratDNA +
      "\nCat DNA: " + catDNA + "\nBat DNA: " + batDNA)

# map init, temp

agents = [ant, rat, cat, bat, antTwo, ratTwo, catTwo, batTwo]

ani = animation.FuncAnimation(fig, mapUpdate, interval=100)

plt.show()
print("let me out")
# while (True):
#    agentMove()
#    mapUpdate()
#    mapPrint()
#    scatterUpdate()
#    print()
#    time.sleep(1)
