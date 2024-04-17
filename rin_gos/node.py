class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getName(self):
        return self.name

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setName(self, name):
        self.name = name

    def __eq__(self, otherNode):
        if self.getName() == otherNode.getName():
            return True
