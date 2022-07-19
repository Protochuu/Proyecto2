from typing import Optional, Tuple, List

from dataclasses import dataclass
from Map import Map

@dataclass
class AVLNode:
    key: str
    value: int

    parent: Optional['AVLNode']
    left_child: Optional['AVLNode'] = None
    right_child: Optional['AVLNode'] = None

    subtree_height: int = 0

    @property
    def has_children(self):
        return (self.left_child is not None) and (self.right_child is not None)


class MapAVL(Map):
    def __init__(self):
        self.root: Optional[AVLNode] = None

    def tree_search(self, key: str) -> Optional[Tuple[str, int]]:
        pass

    def find_insertion_node(self, node: AVLNode, key_to_insert: str) -> AVLNode:
        if node.key == key_to_insert:
            raise KeyError('Llave ya insertada')

        if not node.has_children:
            return node

        if node.key < key_to_insert:
            return self.find_insertion_node(node.right_child, key_to_insert)
        else:
            return self.find_insertion_node(node.left_child, key_to_insert)

    def update_subtrees_from_insertion(self, node: AVLNode):
        node.parent.subtree_height += 1

        if node.parent is self.root:
            return

        self.update_subtrees_from_insertion(node.parent)

    def insert(self, key: str, value: int):
        if self.root is None:
            self.root = AVLNode(key=key,
                                value=value,
                                parent=None)
        else:
            last_node = self.find_insertion_node(self.root, key)

            new_node = AVLNode(key=key,
                               value=value,
                               parent=last_node)

            if last_node.key < key:
                last_node.right_child = new_node
            else:
                last_node.left_child = new_node

            self.update_subtrees_from_insertion(new_node)

    def rebalance(self):
        pass
