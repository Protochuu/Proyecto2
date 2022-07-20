from Map import Map


class MapSV(Map):
    def __init__(self):
        self.inner_list = []

    def binary_insert(self, key: str, value: int):
        left_index = 0
        right_index = len(self.inner_list)

        while right_index - left_index != 0:
            center = (left_index + right_index) // 2
            center_value = self.inner_list[center]

            if center_value[0] == key:
                raise KeyError("Llave ya existente")
            elif center_value[0] < key:
                left_index = center + 1
            elif center_value[0] > key:
                right_index = center

        center = right_index
        self.inner_list.insert(center, (key, value))

    # TODO: REVISAR QUE NO SE TE OLVIDE AAAAAAAAAAAAAAAAAAAAA
    def binary_search(self, key: str):
        left_index = 0
        right_index = len(self.inner_list)

        while right_index - left_index != 0:
            center = (left_index + right_index) // 2
            center_value = self.inner_list[center]

            if center_value[0] == key:
                return center_value
            elif center_value[0] < key:
                left_index = center + 1
            elif center_value[0] > key:
                right_index = center

        return None

    def insert(self, key: str, value: int):
        if len(self.inner_list) == 0:
            self.inner_list.append((key, value))
        else:
            self.binary_insert(key, value)

    def erase(self, key: str):
        removeIndex = None

        if len(self.inner_list) == 0:
            raise IndexError("No hay elementos por eliminar")

        for i in range(len(self.inner_list)):
            element = self.inner_list[i]

            if element[0] == key:
                removeIndex = i

        if removeIndex is None:
            raise KeyError("Llave no encontrada")
        else:
            del self.inner_list[removeIndex]

    def at(self, key: str) -> int:
        search_result = self.binary_search(key)

        if search_result is None:
            raise KeyError("Llave no encontrada")
        else:
            return search_result[1]

    def size(self) -> int:
        return len(self.inner_list)

    def empty(self) -> bool:
        return len(self.inner_list) == 0

if __name__ == "__main__":
    map = MapSV()
    map.insert('ababa', 1)
    map.insert('ebee', 2)
    map.insert('pepe', 3)
    map.insert('aaaaa', 349289)
    map.insert('abaaa', 12341231)
    map.insert('aabaa', 23138123781)

    print(map.at('pepe'))
    print(map.at('aabaa'))
    print(map.at('abaaa'))
    print(map.at('aaaaa'))

    map.insert('wawa', 1313)
    map.erase('wawa')
    print(map.at('wawa'))
