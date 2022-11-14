from random import randint


class Node:
    def __init__(self, from_cell, to_here_cell, board):
        self.children = []
        self.utility = 0
        self.decisionChild = None
        self.from_cell = from_cell
        self.to_here_cell = to_here_cell
        self.board = board

    def setChild(self, child):
        self.children.append(child)

    def setUtility(self, utility):
        self.utility = utility

    def setDecisionChild(self, decisionChild):
        self.decisionChild = decisionChild

    def getDecisionChild(self):
        return self.decisionChild

    def getFromCell(self):
        return self.from_cell

    def getToCell(self):
        return self.to_here_cell

    def setEvaluationFunction(self):
        evaluation = randint(-100, 100)
        self.utility = evaluation
