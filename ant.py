map = [[0, 0], [0, 1]]


def mapTranslate(map):
    returnString = ""
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 1:
                map[i][j] = 0
            else:
                map[i][j] = 1


drawMap(map)
