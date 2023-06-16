import data as dt
import math

# Compute the average cost of the whole training set, to use for training. 
# Calculate the cost for every trainingsset, for every node and add it up. Then device it by the lenght of the trainingsset to get an average.
def computeAverageCost():
    totalCost = 0
    for data in dt.trainingSet:
        nodeIndex = 0
        for irow in range(3):
            for icolumn in range(3):
                inNodes[nodeIndex] = data[0][irow][icolumn]
                nodeIndex += 1
        totalCost += costFunc(sigmoid(multiply(links, inNodes)), dt.outputDict[data[1]])
    return totalCost / len(dt.trainingSet)

# Muliply the link matrix with the inNodes matrix.
# Note: does not work with any matrix!
def multiply(links, inNodes):
    outputVector = []
    for linkRow in links:
        tempValues = []
        for iLink in range(len(linkRow)):
            tempValues.append(linkRow[iLink] * inNodes[iLink])
        outputVector.append(sum(tempValues))
    return outputVector

# Calulates the distance between two vectors.
# Calculate the difference between the given vector and the model vector, then square the differences and return the sum.
def costFunc(outVec, modelVec):
    errors = [abs(zipped[0] - zipped[1]) for zipped in zip(outVec, modelVec)]
    return sum([error*error for error in errors])/len(outVec)

# Makes sure that the given values are between 0 and 1.
def sigmoid(nodes):
    return([1/(1 + math.exp(-node)) for node in nodes])

# Train the neural network by trying to get the lowest possible average cost. 
# For every node, try a weight between -50 and 50, with steps of 0.1. Calculate the average cost for every step. If the average cost went down, save the weight.
# When a node has tried all steps, save the best weight to the node.
def trainWeights(links):
    for irow in range(len(links)):
        for icolumn in range(len(links[0])):
            bestCost = 100000
            bestWeight = 0
            for weight in range(-500, 500):
                links[irow][icolumn] = weight/10
                newCost = computeAverageCost()
                if newCost < bestCost:
                    bestCost = newCost
                    bestWeight = links[irow][icolumn]
            links[irow][icolumn] = bestWeight

if __name__ == "__main__":
    inNodes = [0 for i in range(9)]
    outNodes = [0 for i in range(2)]

    links = [[0 for i in range(9)],
             [0 for i in range(9)]]
    trainWeights(links)

    for set in dt.testSet:
        data = set[0]
        nodeIndex = 0
        for row in range(3):
            for column in range(3):
                inNodes[nodeIndex] = data[row][column]
                nodeIndex += 1
        
        outNodes = multiply(links, inNodes)
        costO = costFunc(sigmoid(outNodes), dt.outputDict['O'])
        costX = costFunc(sigmoid(outNodes), dt.outputDict['X'])
        guessedValue = ""
        if costO > costX: guessedValue = f"X (Certainty: {1-costX})"
        elif costO < costX: guessedValue = f"O (Certainty: {1-costO})"
        else: guessedValue = f"None (Certainty O: {1-costO}, Certainty X {1-costX})"
        print(f"Is: '{set[1]}' \t Guessed: '{guessedValue}'.")