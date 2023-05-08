import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os as os
import math as math
import random as random
import time as time
grid = 11  # 6 actually means like 5 by 5
# y first x second
map = [["O" for i in range(grid - 1)] for j in range(grid - 1)]


def clear():
    os.system('clear')


class agent():
    def __init__(self, name, location, color, handle):
        self.name = name
        self.location = location
        self.graphLocation = graphToMap(location)
        self.oldSpot = location
        self.color = color
        self.handle = handle
        self.children = []

    def action(self):
        # This is going to need to decide between moving, reproducing, eating, constructing. Then call that method. For now lets just use random.
        # this will later need to be based on NN
        decision = random.randint(0, 4)
        if decision > 0:
            self.move()
        elif decision == 0:
            self.construct()
        else:
            print("Dingus")  # just a carry over spot until all methods are made

    def construct(self):
        global leaf
        leafLocal = self.location
        self.children.append(leaf([leafLocal[0], leafLocal[1]], plt.scatter(
            leafLocal[0]-.5, leafLocal[1] - .5, color="darkgreen")))

    def move(self):
        global map
        # 0 = up, 1 = right, 2 = down, 3 = left
        direction = random.randint(0, 3)
        scout = self.location
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
        if map[scoutTranslated[0]][scoutTranslated[1]] == "O":
            self.location = scout

    def update(self):
        global map
        self.handle.remove()
        self.handle = plt.scatter(
            self.location[0]-.5, self.location[1]-.5, color=self.color)
        map[self.graphLocation[0]][self.graphLocation[1]] = "0"
        self.graphLocation = graphToMap(self.location)
        map[self.graphLocation[0]][self.graphLocation[1]] = self
        for child in self.children:
            child.update()


class leaf():
    def __init__(self, location, handle):
        self.location = location
        self.graphLocation = graphToMap(location)
        self.color = "darkgreen"
        self.handle = handle

    def update(self):
        global map
        map[self.graphLocation[0]][self.graphLocation[1]] = self


def agentDecision():
    for i in range(0, len(agents)):
        agents[i].action()


def mapPrint():
    for row in map:
        print(row)
    print()


def mapUpdate(fig):
    for agent in agents:
        agent.update()
    mapPrint()
    global antHandle
    global ratHandle
    agentDecision()


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
    shallow - .5, shallow - .5, color="red"))  # declaration of agents
# will need to think of a less clunky way of doing this

rat = agent("rat", [deep, deep], "blue", plt.scatter(
    deep - .5, deep - .5, color="blue"))

cat = agent("cat", [deep, shallow], "magenta", plt.scatter(
    deep - .5, shallow - .5, color="magenta"))

bat = agent("bat", [shallow, deep], "orange", plt.scatter(
    shallow - .5, deep - .5, color="orange"))

# map init, temp

agents = [ant, rat, cat, bat]

ani = animation.FuncAnimation(fig, mapUpdate, interval=5000)
plt.show()
print("let me out")
# while (True):
#    agentMove()
#    mapUpdate()
#    mapPrint()
#    scatterUpdate()
#    print()
#    time.sleep(1)
