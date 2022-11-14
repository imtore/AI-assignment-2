from minimax import Minimax
from tree import Tree


class RandomMinimaxAgent:
    def __init__(self, myColor, opponentColor):
        self.myColor = myColor
        self.opponentColor = opponentColor
        self.height = 3

    def move(self, board):
        gameTree = Tree(board, self.myColor, self.opponentColor, self.height)
        from_cell, to_cell = Minimax.calNextMove(gameTree, self.height)
        return from_cell, to_cell
