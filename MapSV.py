from Map import Map

class MapSV(Map):
    def __init__(self):
        self.root = None
        self.innerArray = []
    def binaryInsert(self, key: str, value: int):
        center = len(self.innerArray) // 2
        centerValue = self.innerArray[center]
        leftIndex = 0
        rightIndex = len(self.innerArray)
        while True:
            center = (leftIndex + rightIndex) // 2
            if centerValue[0] == key:
                raise KeyError
            elif centerValue[0] < key:
                leftIndex = center + 1
                if rightIndex - leftIndex == 1:
                    self.innerArray.insert(rightIndex, (key, value))
                    break
            elif centerValue[0] > key:
                rightIndex = center
                if rightIndex - leftIndex == 1:
                    self.innerArray.insert(leftIndex, (key, value))
                    break
    def binarySearch:

    def insert(self, key: str, value: int):
        if len(self.innerArray) == 0:
            self.innerArray.append((key,value))
        else:
            self.binaryInsert(key,value)
    def erase(self, key: str):
        if len(self.innerArray) == 0:
            raise IndexError
        for i in range(len(self.innerArray)):
            element = self.innerArray[i]
            if element[0] == key:
                self.innerArray.remove(element)
                return
        raise KeyError
    def at(self, key: str) -> int:
