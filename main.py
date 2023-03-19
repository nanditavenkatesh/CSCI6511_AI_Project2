import copy
import re
from collections import deque


# This function reads the file to get the corresponding colors
def readColor(file):
    with open(file, "r") as f:
        for line in f:
            if "# Colors" in line:
                for line in f:
                    color = int(re.search(r'(?<==).+', line).group(0))
                    return color


# This function reads the file to get a list of nodes and corresponding edges
def readGraph(file):
    with open(file, "r") as f:
        all_nodes = []
        for line in f:
            if "# Graph:" in line:
                for line in f:
                    all_nodes.append(int(line.split(',')[0]))
                    all_nodes.append(int(line.split(',')[1]))
        number_of_nodes = max(all_nodes) + 1
    adjList = [[] for x in range(number_of_nodes)]
    with open(file, "r") as f:
        for line in f:
            if "# Graph:" in line:
                for line in f:
                    edges = line.split(',')
                    adjList[int(edges[0])].append(int(edges[1]))
                    adjList[int(edges[1])].append(int(edges[0]))
    for i in range(number_of_nodes):
        j = list(set(adjList[i]))
        adjList[i] = j
    if not adjList[0]:
        adjList.pop(0)
        for elements in adjList:
            for i in range(len(elements)):
                elements[i] -= 1
    return adjList


# Implementing the AC-3 on the neighbours of the selected node
def ac3Check(nextNode, l, adjList, domainListUpdated):
    while len(l) != 0:
        a = l.popleft()
        [remove, domainListUpdated] = remove_inconsistent_values(a, domainListUpdated)

        if remove == 1:
            if len(domainListUpdated[a[0]]) == 0:
                return 0, domainListUpdated
            adjlistTemp = [item for item in adjList[a[0]] if item != a[1]]

            for j in adjlistTemp:
                b = [j, a[0]]
                if isAssigned[j] != 1:
                    l.append(b)

    return 1, domainListUpdated


# This function removes the domain of connected nodes when one node is assigned with a color
def remove_inconsistent_values(a, domainListUpdated):
    removed = 0
    if len(domainListUpdated[a[1]]) == 1:
        # print("a[1]:",a[1])
        c = domainListUpdated[a[1]][0]
        # print("c:",c)
        if c in domainListUpdated[a[0]]:
            domainListUpdated[a[0]].remove(c)
            removed = 1
    return removed, domainListUpdated


# Implementing the LCV to choose the priority of coloring depending on the restriction a node imposes on its neighbours
def lcv_heuristic(nextNodeChosen, adjList, domainList):
    orderOfColoring = []
    for colors in domainList[nextNodeChosen]:

        minValue = 100
        for i in adjList[nextNodeChosen]:

            noOfColorsRemaining = len(domainList[i])
            if colors in domainList[i]:
                noOfColorsRemaining = noOfColorsRemaining - 1
            if noOfColorsRemaining < minValue:
                minValue = noOfColorsRemaining
        orderOfColoring.append([colors, minValue])
        sortedOrderOfColoring = sorted(orderOfColoring, key=lambda x: x[1], reverse=True)
        colorOrderPriority = [item[0] for item in sortedOrderOfColoring]
    return colorOrderPriority


# Implementing MRV heuristic to choose a node for coloring
def mrv_heuristic(adjList, domainList, assigned):
    minColorsAvailable = 1000
    nextNode = -1
    if 1 in assigned:
        for i in range(Nodes):
            if len(domainList[i]) < minColorsAvailable and assigned[i] != 1:
                minColorsAvailable = len(domainList[i])
                nextNode = i
        return nextNode
    else:
        nextNode = -1
        length = -1
        for x in range(len(adjList)):
            if len(adjList[x]) > length:
                nextNode = x
                length = len(adjList[x])
        return nextNode


# This function checks if the next chosen nodes can have color
def is_possible(nextNodeChosen, color, colorAssigned, adjList):
    for j in adjList[nextNodeChosen]:
        if color == colorAssigned[j]:
            return 0
    return 1


# Implementing CSP for the Graph Coloring Problem
def backtrack(colorAssigned, adjList, domainList, isAssigned):
    if -1 not in isAssigned:
        # print(colorAssigned)
        return colorAssigned
    nextNodeChosen = mrv_heuristic(adjList, domainList, isAssigned)
    coloringOrder = lcv_heuristic(nextNodeChosen, adjList, domainList)
    for color in coloringOrder:
        domainListUpdated = copy.deepcopy(domainList)
        if is_possible(nextNodeChosen, color, colorAssigned, adjList):
            domainListUpdated[nextNodeChosen] = [item for item in domainList[nextNodeChosen] if item == color]
            arrayTemp = []
            for j in adjList[nextNodeChosen]:
                a = [j, nextNodeChosen]
                if isAssigned[j] != 1:
                    arrayTemp.append(a)
                l = deque(arrayTemp)
            [ac3CheckResult, dlist] = ac3Check(nextNodeChosen, l, adjList, domainListUpdated)
            if ac3CheckResult == 1:
                colorAssigned[nextNodeChosen] = color
                isAssigned[nextNodeChosen] = 1
                domainListUpdated = dlist
                result = backtrack(colorAssigned, adjList, domainListUpdated, isAssigned)
                if result != 0:
                    return result
        colorAssigned[nextNodeChosen] = -1
        isAssigned[nextNodeChosen] = -1
    return 0



def main(file):
    global Nodes
    global isAssigned

    adjList = readGraph(file)
    Nodes = len(adjList)
    Colors = readColor(file)
    # print("File Reading Complete")

    colorAssigned = [-1 for i in range(Nodes)]
    isAssigned = [-1 for i in range(Nodes)]

    domainList = [[] for k in range(Nodes)]
    for i in range(0, Nodes):
        for j in range(0, Colors):
            domainList[i].append(j)

    coloringResult = backtrack(colorAssigned, adjList, domainList, isAssigned)
    if coloringResult == 0:
        print("No answer")
        return False
    else:
        print(coloringResult)
        for i in range(Nodes):
            for j in adjList[i]:
                if coloringResult[i] == coloringResult[j]:
                    print("error")
                    return False
    print("No error")
    return True


if __name__ == "__main__":
    # file = "inputFiles/gc_78317094521100.txt"
    # file = "inputFiles/gc_78317097930400.txt"
    # file = "inputFiles/gc_78317097930401.txt"
    # file = "inputFiles/gc_78317100510400.txt"
    # file = "inputFiles/gc_78317103208800.txt"
    # file = "inputFiles/gc_1377121623225900.txt"
    # file = "inputFiles/gc_1378296846561000.txt"
    file = "inputFiles/test.txt"
    main(file)
