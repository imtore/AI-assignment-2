import copy
from node import Node


class Tree:
    def __init__(self, board, color, opponentColor, height):
        self.height = height
        self.board = board
        self.nodes = [[] for i in range(self.height+1)]
        self.root = self.makeNode(0, board)
        self.buildTree(color, opponentColor)

    def makeNode(self, height, board, from_cell=None, to_cell=None):
        node = Node(from_cell, to_cell, board)
        self.nodes[height].append(node)
        return node

    def buildTree(self, color, opponentColor):
        maxNodes = [self.root]
        minNodes = []
        maxTurn = True
        for i in range(self.height):
            if maxTurn:
                minNodes = self.makeMinimaxChildrenFor(maxNodes, color, opponentColor, i+1)
                maxTurn = False
            else:
                maxNodes = self.makeMinimaxChildrenFor(minNodes, opponentColor, color, i+1)
                maxTurn = True

    def makeMinimaxChildrenFor(self, nodes, color, opponentColor, height):
        resultNodes = []
        for node in nodes:
            if node.board.win(color) or node.board.win(opponentColor):
                node.setEvaluationFunction()
                continue
            else:
                piecesFromCell, piecesToCell = node.board.getPiecesPossibleLocations(color)
                for i in range(len(piecesToCell)):
                    for j in range(len(piecesToCell[i])):
                        newBoard = copy.deepcopy(node.board)
                        newBoard.changePieceLocation(color, piecesFromCell[i], piecesToCell[i][j])

                        childNode = self.makeNode(height, newBoard, piecesFromCell[i], piecesToCell[i][j])
                        resultNodes.append(childNode)

                        node.setChild(childNode)

        return resultNodes
