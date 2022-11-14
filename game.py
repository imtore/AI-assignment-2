from RandomMinimaxAgent import RandomMinimaxAgent
from agent import Agent
from board import Board
import time
from graphicalBoard import GraphicalBoard


def printBoard(board):
    boardList = board.board
    for i in range(board.n_rows):
        print(boardList[i])
    print()


def switchTurn(turn):
    if turn == 'W':
        return 'B'
    return 'W'


def play(white, black, board):
    # graphicalBoard = GraphicalBoard(board)
    turn = 'W'
    while not board.finishedGame():
        if turn == 'W':
            from_cell, to_cell = white.move(board)
        elif turn == 'B':
            from_cell, to_cell = black.move(board)
        else:
            raise Exception
        board.changePieceLocation(turn, from_cell, to_cell)
        printBoard(board)
        turn = switchTurn(turn)
        # graphicalBoard.showBoard()


if __name__ == '__main__':
    board = Board(6, 6, 2)
    white = RandomMinimaxAgent('W', 'B')
    you = Agent('B', 'W')
    play(white, you, board)
