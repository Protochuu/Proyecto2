
class Node(object):
    def __init__(self):
        self.root = []
        self.children = [None]

    def insert(self,pairLeaf):
        self.root.append(pairLeaf)
        self.root.sort()
        print(self.children)

        if len(self.root) == 5:
            print("se entro en el if")
            leafLeft = self.root[0:2]
            leafRight = self.root[3:]
            leafCenter = self.root[2]
            print((leafCenter))
            print(leafLeft)
            print(leafRight)
        else:
            self.children.append(None)



gatos = Node()
gatos.insert(("popo",1))
gatos.insert(("popo",4))
gatos.insert(("popo",2))
gatos.insert(("popo",6))
gatos.insert(("popo",5))

perros = Node()
gatos.children[0] = perros
print(gatos.children)