from Map import Map

class MapSV(Map):
    def __init__(self):
        self.root = None
        self.innerArray = []

    def binaryInsert(self, key: str, value: int):
        leftIndex = 0
        rightIndex = len(self.innerArray)

        while rightIndex - leftIndex != 0:
            center = (leftIndex + rightIndex) // 2
            centerValue = self.innerArray[center]

            if centerValue[0] == key:
                raise KeyError
            elif centerValue[0] < key:
                leftIndex = center + 1
            elif centerValue[0] > key:
                rightIndex = center

        center = rightIndex
        self.innerArray.insert(center, (key, value))


    def binarySearch(self,key : str):
        leftIndex = 0
        rightIndex = len(self.innerArray)
        while rightIndex - leftIndex != 1:
            center = (leftIndex + rightIndex) // 2
            centerValue = self.innerArray[center]
            if centerValue[0] == key:
                return centerValue
            elif centerValue[0] < key:
                leftIndex = center + 1
            elif centerValue[0] > key:
                rightIndex = center
        return None

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
        searchResult = self.binarySearch(key)
        if searchResult is None:
            raise KeyError
        else:
            return searchResult[1]

    def size(self) -> int:
        return len(self.innerArray)

    def empty(self) -> bool:
        return len(self.innerArray) == 0

if __name__ == "__main__":
    gatos = MapSV()

    gatos.insert("a", 1)
    gatos.insert("b", 2)
    gatos.insert("c", 3)
    gatos.insert("d", 4)
    gatos.insert("e", 5)

    print(gatos.innerArray)