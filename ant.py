import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os as os
import math as math
import random as random
import time as time
grid = 11  # 6 actually means like 5 by 5
# y first x second
map = [["O" for i in range(grid)] for j in range(grid)]


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class agent():
    def __init__(self, name, location, color, handle):
        self.name = name
        self.location = location
        self.color = color
        self.handle = handle

    def move(self):
        # 0 = up, 1 = right, 2 = down, 3 = left
        direction = random.randint(0, 3)
        if direction == 0:
            if self.location[0] == 0.5:
                self.location[0] = grid - 1.5
            else:
                self.location[0] -= 1
        elif direction == 1:
            if self.location[1] == grid - 1.5:
                self.location[1] = 0.5
            else:
                self.location[1] += 1
        elif direction == 2:
            if self.location[0] == grid - 1.5:
                self.location[0] = 0.5
            else:
                self.location[0] += 1
        elif direction == 3:
            if self.location[1] == 0.5:
                self.location[1] = grid - 1.5
            else:
                self.location[1] -= 1


def mapUpdate():
    global map
    map = [["O" for i in range(grid)] for j in range(grid)]
    for i in range(0, len(agents)):
        map[agents[i].location[0]][agents[i].location[1]] = agents[i].image


def agentMove():
    for i in range(0, len(agents)):
        agents[i].move()


def mapPrint():
    for row in map:
        print(row)
        print()


def mapUpdate(fig):
    # fig.clear()
    global antHandle
    global ratHandle
    agentMove()
    # for agent in agents:
    for agent in agents:
        agent.handle.remove()
        agent.handle = plt.scatter(
            agent.location[0], agent.location[1], color=agent.color)


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

ant = agent("ant", [0.5, 0.5], "red", plt.scatter(
    0.5, 0.5, color="red"))  # declaration of agents
# will need to think of a less clunky way of doing this
rat = agent("rat", [grid - 1.5, grid - 1.5], "blue", plt.scatter(
    grid - 1.5, grid - 1.5, color="blue"))
cat = agent("cat", [grid - 1.5, 0.5], "green", plt.scatter(
    grid - 1.5, 0.5, color="green"))
bat = agent("bat", [0.5, grid - 1.5], "orange", plt.scatter(
    0.5, grid - 1.5, color="orange"))

agents = [ant, rat, cat, bat]

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
