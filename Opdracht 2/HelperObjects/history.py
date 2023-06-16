class CompositionHistory:
    compositions : list
    userRatings : list

    def __init__(self, compositions: list = [], userRatings: list = []):
        self.compositions = compositions
        self.userRatings = userRatings
    
    def toDict(self) -> dict:
        return self.__dict__