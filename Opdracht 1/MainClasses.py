import data as dt
import math
from Node import *
from Link import *

# Compute the average cost of the whole training set, to use for training. 
# Calculate the cost for every trainingsset, for every node and add it up. Then device it by the lenght of the trainingsset to get an average.
def computeAverageCost():
    totalCost = 0
    for data in dt.trainingSet:
        for row in range(3):
            for column in range(3):
                inNodes[row][column].storedValue = data[0][row][column]
        totalCost += costFunc(softMax([outNode.getValue() for outNode in outNodes]), dt.outputDict[data[1]])
    return totalCost / len(dt.trainingSet)

# Calulates the distance between two vectors.
# Calculate the difference between the given vector and the model vector, then square the differences and return the sum.
def costFunc(outVec, modelVec):
    errors = [abs(zipped[0] - zipped[1]) for zipped in zip(outVec, modelVec)]
    return sum([error*error for error in errors])/len(outVec)

# Makes sure that the given values add up to 1.
# For every node, raise e to the power of the node. Then take the sum of all these nodes, and devide every e^X node by this sum.
def softMax(nodes):
    eNodes = [math.exp(node) for node in nodes]
    eTotal = sum(eNodes)
    return([node / eTotal for node in eNodes])

# Train the neural network by trying to get the lowest possible average cost. 
# For every node, try a weight between -50 and 50, with steps of 0.1. Calculate the average cost for every step. If the average cost went down, save the weight.
# When a node has tried all steps, save the best weight to the node.
def trainWeights(links):
    for link in links:
        bestCost = 100000
        bestWeight = 0
        for weight in range(-500, 500):
            link.weight = weight/10
            newCost = computeAverageCost()
            if newCost < bestCost:
                bestCost = newCost
                bestWeight = link.weight
        link.weight = bestWeight

if __name__ == "__main__":
    inNodes = [[Node() for i in range(3)],
                [Node() for i in range(3)],
                [Node() for i in range(3)]]
    outNodes = [Node() for i in range(2)]

    links = []
    for inRow in inNodes:
        for inNode in inRow:
            for outNode in outNodes:
                links.append(Link(inNode, outNode))
    trainWeights(links)

    for set in dt.testSet:
        data = set[0]
        for row in range(3):
            for column in range(3):
                inNodes[row][column].storedValue = data[row][column]
        costO = costFunc(softMax([outNode.getValue() for outNode in outNodes]), dt.outputDict['O'])
        costX = costFunc(softMax([outNode.getValue() for outNode in outNodes]), dt.outputDict['X'])
        if costO > costX: guessedValue = f"X (Certainty: {1-costX})"
        elif costO < costX: guessedValue = f"O (Certainty: {1-costO})"
        else: guessedValue = f"None (Certainty O: {1-costO}, Certainty X {1-costX})"
        print(f"Is: '{set[1]}' \t Guessed: '{guessedValue}'.")