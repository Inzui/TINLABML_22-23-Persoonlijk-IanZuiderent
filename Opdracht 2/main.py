import json, os, math, copy
from itertools import chain
from HelperObjects.history import CompositionHistory
from Services.compositionBuilder import CompositionBuilder

class Main():
    def __init__(self, debugMode: bool = False):
        self.debugMode = debugMode
        self.historyFileName = "HistoryData.json"
        self.compositionBuilder = CompositionBuilder(os.path.join(os.getcwd(), "Songs"))
    
    def run(self):
        compositionHistory = self.readHistoryFromDisk()
        if (compositionHistory == None):
            compositionHistory = CompositionHistory()
        else:
            self.compositionBuilder.composition = copy.deepcopy(compositionHistory.compositions[-1])
            self.compositionBuilder.userRatings = copy.deepcopy(compositionHistory.userRatings[-1])

        while True:
            # Randomly generate the first 3 generations so there is more variation at the beginning.
            if (len(compositionHistory.compositions) < 3):
                self.compositionBuilder.composeRndGen(len(compositionHistory.compositions))
            else:
                self.compositionBuilder.composeNewGen(compositionHistory)    

            if (not self.debugMode):
                self.generateWav(len(compositionHistory.compositions))
            self.compositionBuilder.userRatings = self.getUserRatings()
            compositionHistory.compositions.append(copy.deepcopy(self.compositionBuilder.composition))
            compositionHistory.userRatings.append(copy.deepcopy(self.compositionBuilder.userRatings))
            self.writeHistoryToDisk(compositionHistory)
    
    def getUserRatings(self) -> list:
        userRatings = []
        predictedLength = math.ceil(60 / self.compositionBuilder.bpm * (self.compositionBuilder.amountOfBars * self.compositionBuilder.barSize))
        for i in range(self.compositionBuilder.amountOfBars):
            userInput = '0'
            while (len(userInput) != 1 or userInput < '1' or userInput > '5'):
                print(f"Rate part {i+1}/{self.compositionBuilder.amountOfBars} from 1 to 5. ({predictedLength/self.compositionBuilder.amountOfBars * i}s - {predictedLength/self.compositionBuilder.amountOfBars * (i+1)}s)")
                userInput = input()
            userRatings.append(int(userInput))
        return userRatings
    
    def generateWav(self, generationNumber: int):
        self.compositionBuilder.processedComposition = [[],[]]
        self.compositionBuilder.processedComposition[0] = list(chain.from_iterable(self.compositionBuilder.composition[0]))
        self.compositionBuilder.processedComposition[1] = list(chain.from_iterable(self.compositionBuilder.composition[1]))
        self.compositionBuilder.muser.generate(self.compositionBuilder.processedComposition, generationNumber)
    
    def writeHistoryToDisk(self, data: CompositionHistory):
        with open(self.historyFileName, "w") as outJson:
            outJson.write(json.dumps(data.toDict()))
    
    def readHistoryFromDisk(self) -> CompositionHistory:
        if (os.path.isfile(self.historyFileName)):
            with open(self.historyFileName) as jsonFile:
                return CompositionHistory(**json.load(jsonFile))
        else:
            return None

if __name__ == "__main__":
    main = Main(debugMode = False)
    main.run()