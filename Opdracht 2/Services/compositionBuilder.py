from HelperObjects.history import CompositionHistory
import Services.muser as ms, random, heapq

class CompositionBuilder():
    def __init__(self, songDirectory: str, bpm: int = 130, barSize: int = 10, amountOfBars: int = 8):
        self.muser = ms.Muser(bpm, songDirectory)
        self.bpm = bpm
        self.barSize = barSize
        self.amountOfBars = amountOfBars

        self.composition = [[], []]
        self.userRatings = []
        self.processedComposition = []

        self.noteLengths = (2, 4, 8, 16, 32)
        self.noteList = ("a0", "a#0", "b0",
         "c1", "c#1", "d1", "d#1", "e1", "f1", "f#1", "g1", "g#1", "a1", "a#1", "b1", 
         "c2", "c#2", "d2", "d#2", "e2", "f2", "f#2", "g2", "g#2", "a2", "a#2", "b2", 
         "c3", "c#3", "d3", "d#3", "e3", "f3", "f#3", "g3", "g#3", "a3", "a#3", "b3", 
         "c4", "c#4", "d4", "d#4", "e4", "f4", "f#4", "g4", "g#4", "a4", "a#4", "b4", 
         "c5", "c#5", "d5", "d#5", "e5", "f5", "f#5", "g5", "g#5", "a5", "a#5", "b5", 
         "c6", "c#6", "d6", "d#6", "e6", "f6", "f#6", "g6", "g#6", "a6", "a#6", "b6", 
         "c7", "c#7", "d7", "d#7", "e7", "f7", "f#7", "g7", "g#7", "a7", "a#7", "b7", 
        "c8")

        self.buildingBlocks = [[["d#7", "g7", "c7"], ["d#5", "g5", "c5"]],
                               [["a4", "c#4", "e4"], ["a4", "c#4", "e4"]],
                               [["a5", "c5", "e5"], ["a3", "c3", "e3"]],
                               [["d1", "f#1", "a1"], ["d1", "f#1", "a1"]],
                               [["d6", "f6", "a6"], ["d6", "f6", "a6"]],
                               [["e4", "g#4", "b4"], ["e5", "g#5", "b5"]],
                               [["e4", "g4", "b4"], ["e7", "g7", "b7"]],
                               [["f5", "a5", "c5"], ["f2", "a2", "c2"]],
                               [["g6", "b6", "d6"], ["g5", "b5", "d5"]]]
    
    def composeRndGen(self, generationNumber: int):
        print(f"\nRandomly generating generation #{generationNumber}:")
        for i in range(self.amountOfBars):
            if (len(self.composition[0]) < self.amountOfBars):
                self.composition[0].append([])
                self.composition[1].append([])
            self.composition[0][i], self.composition[1][i] = self.getBarRnd()
        self.printGeneration(self.composition)

    def composeNewGen(self, history: CompositionHistory):
        print(f"\nGenerating generation #{len(history.compositions)}:")

        # Genetic Purging: Remove the x worst generations from the gene pool.
        amountToRemove = int(len(history.compositions) / 5)
        if (amountToRemove > 0):
            self.removeBadGenerations(history, amountToRemove)

        # Crossover: Get two good scoring previous generations, and cross them.
        genCross1, genCross2 = self.getRndGenerations(history)
        self.composition[0], self.composition[1] = self.crossGenerations(genCross1, genCross2)
        
        # Elitism: Get the two best bars from the previous generation and just place them in the composition.
        bestBarIndexes = heapq.nlargest(2, range(len(history.userRatings[-1])), key = history.userRatings[-1].__getitem__)
        for i in bestBarIndexes:
            self.composition[0][i] = history.compositions[-1][0][i]
            self.composition[1][i] = history.compositions[-1][1][i]
        print(f"Placed bars {bestBarIndexes} from the previous generation into the new generation.")

        # Mutation: Make some random changes to the bars, except for the bars that have been copied in the elitism step.
        self.mutateGeneration(self.composition, bestBarIndexes)
        print("New generation:")
        self.printGeneration(self.composition)

    def removeBadGenerations(self, history: CompositionHistory, amountToRemove: int):
        print(f"Removing the {amountToRemove} worst generations.")
        worstGenerationIndexes = set(heapq.nsmallest(amountToRemove, range(len(history.userRatings)), key = history.userRatings.__getitem__))

        toRemoveListComp = []
        toRemoveListRat = []
        for i in worstGenerationIndexes:
            toRemoveListComp.append(history.compositions[i])
            toRemoveListRat.append(history.userRatings[i])
        
        for composition in toRemoveListComp:
            history.compositions.remove(composition)
        for rating in toRemoveListRat:
            history.userRatings.remove(rating)

        print(f"Removed generation(s) #{worstGenerationIndexes}")
    
    # Mutate a generation by randomizing at least one random bar in the generation.
    def mutateGeneration(self, gen: list, excludeBarsIndexes: list):
        mutatedBars = []
        while(len(mutatedBars) < 1):
            for barIndex in range(self.amountOfBars):
                if (not barIndex in mutatedBars and not barIndex in excludeBarsIndexes):
                    mutateBar = random.randint(0, 10) == 0
                    if (mutateBar):
                        gen[0][barIndex], gen[1][barIndex] = self.getBarRnd()
                        mutatedBars.append(barIndex)
        print(f"Mutated bar(s) {mutatedBars}.")

    # Cross two generations by splitting them at a random point, and then paste them together.
    def crossGenerations(self, gen1: list, gen2: list) -> list:
        crossPoint = random.randint(1, self.amountOfBars - 2)
        track1 = [gen1[0][barIndex] if barIndex < crossPoint else gen2[0][barIndex] for barIndex in range(self.amountOfBars)]
        track2 = [gen1[1][barIndex] if barIndex < crossPoint else gen2[1][barIndex] for barIndex in range(self.amountOfBars)]

        print(f"Crossed at bar #{crossPoint}.")
        return track1, track2

    # Get two random previous generations. The higher the overall score, the better the chance of getting selected.
    def getRndGenerations(self, history: CompositionHistory) -> list:
        gen1 = None

        while True:
            for genIndex in range(len(history.compositions)):
                score = sum(history.userRatings[genIndex])
                if (random.randint(0, 5 * (self.amountOfBars + 1) - score) == 0):
                    print(f"Selected gen #{genIndex}:")
                    self.printGeneration(history.compositions[genIndex])
                    if (gen1 == None):
                        gen1 = history.compositions[genIndex]
                    else:
                        return gen1, history.compositions[genIndex]
    
    # Get random bars by either generating completely new ones or getting a building block. 
    def getBarRnd(self) -> list:
        randomizeBar = random.randint(0, 1) == 0
        if (randomizeBar):
            return self.generateBarRnd(), self.generateBarRnd()
        else:
            buildingBlockIndex = random.randint(0, len(self.buildingBlocks) - 1)
            return self.getBuildingBlockRnd(buildingBlockIndex)

    # Get a building block and randomize its timing.
    def getBuildingBlockRnd(self, buildingBlockIndex: int) -> list:
        buildingBlock = self.buildingBlocks[buildingBlockIndex]
        barTrack1 = []
        barTrack2 = []

        barSizeLeft = self.barSize
        for noteIndex in range(len(buildingBlock[0])):
            if (noteIndex == len(buildingBlock[0]) - 1):
                if (barSizeLeft == 0):
                    noteLength = 2
                    if (barTrack1[0][1] != 2):
                        barTrack1[0][1] -= 2
                        barTrack2[0][1] -= 2
                    else:
                        barTrack1[1][1] -= 2
                        barTrack2[1][1] -= 2
                else:
                    noteLength = barSizeLeft
            else:
                noteLength = random.choice(self.noteLengths)
                while (barSizeLeft - noteLength < 0):
                    noteLength = random.choice(self.noteLengths)
            barSizeLeft -= noteLength
            barTrack1.append([buildingBlock[0][noteIndex], noteLength])
            barTrack2.append([buildingBlock[1][noteIndex], noteLength])
        
        return barTrack1, barTrack2

    # Generate a bar with random notes and timing.
    def generateBarRnd(self) -> list:
        bar = []
        barSizeLeft = self.barSize
        while (barSizeLeft > 0):
            noteLength = random.choice(self.noteLengths)
            while (barSizeLeft - noteLength < 0):
                noteLength = random.choice(self.noteLengths)
            barSizeLeft -= noteLength
            bar.append([random.choice(self.noteList), noteLength])
        return bar
    
    def printGeneration(self, gen: list):
        print("Track 1 \t | \t Track 2")
        for i in range(self.amountOfBars):
            print(f"Bar #{i}: {gen[0][i]} \t | \t {gen[1][i]}")