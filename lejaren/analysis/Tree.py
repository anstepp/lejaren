from .Node import Node

class Tree:
    nodeList = []

    def __init__(self):
        self.nodeList = []

    def makeTree(self):
        self.nodeList.sort(self.nodeList, key=lambda node: node.location)
        for current_node in self.nodeList:
            continue

    def searchTree(self):
        pass

    def getBoundaries(self):
        pass
