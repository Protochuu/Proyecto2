from Map import Map


class MapSV(Map):

    def __init__(self):

        self.root = None
        self.inner_array = []

    def binary_insert(self, key: str, value: int):
        left_index = 0
        right_index = len(self.inner_array)

        while right_index - left_index != 0:
            center = (left_index + right_index) // 2
            center_value = self.inner_array[center]

            if center_value[0] == key:
                raise KeyError
            elif center_value[0] < key:
                left_index = center + 1
            elif center_value[0] > key:
                right_index = center

        center = right_index
        self.inner_array.insert(center, (key, value))

    def binary_search(self, key: str):
        left_index = 0
        right_index = len(self.inner_array)
        while right_index - left_index != 1:
            center = (left_index + right_index) // 2
            center_value = self.inner_array[center]
            if center_value[0] == key:
                return center_value
            elif center_value[0] < key:
                left_index = center + 1
            elif center_value[0] > key:
                right_index = center
        return None

    def insert(self, key: str, value: int):
        if len(self.inner_array) == 0:
            self.inner_array.append((key, value))
        else:
            self.binary_insert(key, value)

    def erase(self, key: str):
        if len(self.inner_array) == 0:
            raise IndexError
        for i in range(len(self.inner_array)):
            element = self.inner_array[i]
            if element[0] == key:
                self.inner_array.remove(element)
                return
        raise KeyError

    def at(self, key: str) -> int:
        search_result = self.binary_search(key)
        if search_result is None:
            raise KeyError
        else:
            return search_result[1]

    def size(self) -> int:
        return len(self.inner_array)

    def empty(self) -> bool:
        return len(self.inner_array) == 0
