class Link:
    def __init__(self, inNode, outNode, weight = 1):
        self.weight = weight
        self.inNode = inNode
        outNode.links.append(self)
    
    def getValue(self):
        return self.inNode.getValue() * self.weight