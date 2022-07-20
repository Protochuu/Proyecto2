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
        return (self.left_child is not None) or (self.right_child is not None)

    @property
    def is_leaf(self):
        return not self.has_children

    @property
    def has_one_child(self):
        return bool(self.left_child is not None) ^ bool(self.right_child is not None)

    @property
    def only_child(self):
        if self.has_one_child:
            return self.left_child if self.left_child is not None else self.right_child
        else:
            raise AttributeError


class MapAVL(Map):
    def __init__(self):
        self.root: Optional[AVLNode] = None

    def find_insertion_node(self, node: AVLNode, key_to_insert: str) -> AVLNode:
        if node.key == key_to_insert:
            raise KeyError('Llave ya insertada.')

        if not node.has_children:
            return node

        if node.key < key_to_insert:
            return self.find_insertion_node(node.right_child, key_to_insert)
        else:
            return self.find_insertion_node(node.left_child, key_to_insert)

    def rotate_left(self, node_to_balance: AVLNode):
        right_child = node_to_balance.right_child
        node_to_balance.right_child = right_child.left_child

        node_to_balance.subtree_height = 1 + max(node_to_balance.right_child.subtree_height,
                                                 node_to_balance.left_child.subtree_height)

        right_child.subtree_height = 1 + max(node_to_balance.right_child.subtree_height,
                                             node_to_balance.left_child.subtree_height)

        if node_to_balance.parent is None:
            right_child.parent = None
            self.root = right_child
        else:
            right_child.parent = node_to_balance.parent

            node_to_balance.parent.left_child = right_child
            node_to_balance.parent = right_child

        right_child.left_child = node_to_balance

    def rotate_right(self, node_to_balance: AVLNode):
        left_child = node_to_balance.left_child

        node_to_balance.right_child = left_child.right_child

        node_to_balance.subtree_height = 1 + max(node_to_balance.right_child.subtree_height,
                                                 node_to_balance.left_child.subtree_height)

        left_child.subtree_height = 1 + max(node_to_balance.right_child.subtree_height,
                                             node_to_balance.left_child.subtree_height)

        if node_to_balance.parent is None:
            left_child.parent = None
            self.root = left_child
        else:
            left_child.parent = node_to_balance.parent

            node_to_balance.parent.left_child = left_child
            node_to_balance.parent = left_child

        left_child.right_child = node_to_balance

    def rotate_left_right(self, node_to_balance: AVLNode):
        self.rotate_left(node_to_balance.right_child)
        self.rotate_right(node_to_balance)

    def rotate_right_left(self, node_to_balance: AVLNode):
        self.rotate_right(node_to_balance.left_child)
        self.rotate_left(node_to_balance)

    def rebalance_from(self, node: AVLNode):
        if not(node.left_child and node.right_child):
            return

        height_difference = (node.left_child.subtree_height
                             - node.right_child.subtree_height)

        if height_difference > 1:
            left_child = node.left_child
            middle_child = left_child.right_child

            if middle_child.key < left_child.key:
                self.rotate_right(node)
            else:
                self.rotate_left_right(node)

        elif height_difference < -1:
            right_child = node.right_child
            middle_child = right_child.left_child

            if middle_child.key > right_child.key:
                self.rotate_left(node)
            else:
                self.rotate_left_right(node)

    def update_subtrees_from_insertion(self, node: AVLNode):
        self.rebalance_from(node)

        parent_node = node.parent
        parent_node.subtree_height += 1

        if parent_node is self.root:
            return

        self.update_subtrees_from_insertion(parent_node)

    def tree_search(self, key: str) -> Optional[Tuple[str, int]]:
        pass

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

    def find_erase_node(self, node: AVLNode, key_to_insert: str) -> AVLNode:
        if node.key == key_to_insert:
            raise KeyError('Llave ya insertada.')

        if not node.has_children:
            return node

        if node.key < key_to_insert:
            return self.find_insertion_node(node.right_child, key_to_insert)
        else:
            return self.find_insertion_node(node.left_child, key_to_insert)

    @staticmethod
    def _delete_node( node: AVLNode):
        parent_node = node.parent

        if parent_node.left_child is node:
            parent_node.left_child = None

        if parent_node.right_child is node:
            parent_node.right_child = None

        del node

    def find_successor(self, node: AVLNode, _root: bool = True) -> AVLNode:
        if not node.has_children:
            return node

        if _root:
            self.find_successor(node.left_child, False)
        else:
            self.find_successor(node.right_child, False)

    def erase(self, key: str):
        node_to_erase = self.find_erase_node(self.root, key)
        current_node = None

        if node_to_erase.is_leaf:
            self._delete_node(node_to_erase)

        elif node_to_erase.has_one_child:
            only_child = node_to_erase.only_child
            parent = node_to_erase.parent

            if parent.left_child is node_to_erase:
                parent.left_child = only_child
            else:
                parent.right_child = only_child

            only_child.subtree_height = node_to_erase.subtree_height

            current_node = only_child
        else:
            successor = self.find_successor(node_to_erase)
            node_to_erase.key = successor.key
            node_to_erase.value = successor.value

            self._delete_node(successor)

            current_node = node_to_erase

        if current_node is not None:
            self.rebalance_from(current_node)

    #TODO: LISTO
    def search_node(self, node: AVLNode, key: str) -> Optional[AVLNode]:
        if node is None:
            return None

        if node.key < key:
            return self.search_node(node.right_child, key)
        else:
            return self.search_node(node.left_child, key)

    #TODO: LISTO
    def at(self, key: str) -> int:
        if result := self.search_node(self.root, key):
            return result.value
        else:
            raise KeyError

    def print(self):
        pass
