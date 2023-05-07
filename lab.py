import matplotlib.pyplot as plt
import numpy as np

# grid init
x = [0, 0, 0, 0, 0, 0, 0, 0, 0]
y = [x, x, x, x, x, x, x, x, x]

grid = np.array(y)

x = np.linspace(0, 2)
y = np.linspace(0, 2)

fig, ax = plt.subplots()
ax.plot(x, y)

ax.fill_between(x, y, 0, where=x < 1, facecolor='green')

plt.grid(True)

plt.show()
