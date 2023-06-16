class Node:
    def __init__(self):
        self.links = []
        self.storedValue = None
    
    def getValue(self):
        if self.links:
            sum = 0
            for link in self.links:
                sum += link.getValue()
            return sum
        else:
            return self.storedValue