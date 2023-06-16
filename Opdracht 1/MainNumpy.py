import data as dt
import numpy as np
import math
from datetime import datetime

# Compute the average cost of the whole training set, to use for training. 
# Calculate the cost for every trainingsset, for every node and add it up. Then devide it by the lenght of the trainingsset to get an average.
def computeAverageCost():
    totalCost = 0
    for data in dt.trainingSet:
        nodeIndex = 0
        for irow in range(3):
            for icolumn in range(3):
                inNodes.itemset(nodeIndex, data[0][irow][icolumn])
                nodeIndex += 1
        totalCost += costFunc(sigmoid(links * inNodes), dt.outputDict[data[1]])
    return totalCost / len(dt.trainingSet)

# Calulates the distance between two vectors.
# Calculate the difference between the given vector and the model vector, then square the differences and return the sum.
def costFunc(outVec, modelVec):
    errors = [abs(zipped[0] - zipped[1]) for zipped in zip(outVec, modelVec)]
    return sum([error*error for error in errors])/len(outVec)

# Makes sure that the given values are between 0 and 1.
def sigmoid(nodes):
    return([1/(1 + math.exp(-node)) for node in nodes])

# Train the neural network by trying to get the lowest possible average cost. 
# For every link, add the learningRate. Then only keep the change that made the most impact on lowering the average cost.
def trainWeights(links):
    avgCost = computeAverageCost()
    learningRate = 0.1

    while (avgCost >= dt.maxCost):
        bestDifference = 0.0
        bestLinkIndex = None
        bestLinkRanges = None
        linkIndex = 0
        for row in range(len(links)):
            for link in range(links[row].size):
                links.itemset(linkIndex, links[row, link] + learningRate)
                newCost = computeAverageCost()
                difference = newCost - avgCost
                if (difference < bestDifference):
                    bestLinkIndex = linkIndex
                    bestDifference = difference
                    bestLinkRanges = row, link
                links.itemset(linkIndex, links[row, link] - learningRate)
                linkIndex += 1
        links.itemset(bestLinkIndex, links[bestLinkRanges] + learningRate)
        avgCost = computeAverageCost()

if __name__ == "__main__":
    inNodes = np.matrix([[0.0] for i in range(9)])
    outNodes = np.matrix([0.0 for i in range(2)])
    links = np.matrix([[-5.0 for i in range(9)],
                        [-5.0 for i in range(9)]])
    
    startTrainingTime = datetime.now()
    print("Started training...")
    trainWeights(links)
    print(f"Training completed in: {(datetime.now() - startTrainingTime).total_seconds()}s.")

    for set in dt.testSet:
        data = set[0]
        nodeIndex = 0
        for irow in range(3):
            for icolumn in range(3):
                inNodes.itemset(nodeIndex, data[irow][icolumn])
                nodeIndex += 1
        
        outNodes = links * inNodes
        costO = costFunc(sigmoid(outNodes), dt.outputDict['O'])
        costX = costFunc(sigmoid(outNodes), dt.outputDict['X'])

        guessedValue = ""
        if costO > costX: guessedValue = f"X (Certainty: {1-costX})"
        elif costO < costX: guessedValue = f"O (Certainty: {1-costO})"
        else: guessedValue = f"None (Certainty O: {1-costO}, Certainty X {1-costX})"
        print(f"Is: '{set[1]}' \t Guessed: '{guessedValue}'.")