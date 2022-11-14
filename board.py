################################
#         B  B  B  ‌‌‌‌B B
#         B  B  B  B B
#         E  E  E  E E
#         E  E  E  E E
#         W  W  W  W W
#         W  W  W  W W
################################


class Board:
    def __init__(self, n_rows=6, n_cols=6, player_row_number=2):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.PLAYER_ROW_NUMBER = player_row_number
        self.board = self.initilizeBoard()

    def initilizeBoard(self):
        resultBoard = []
        for i in range(self.PLAYER_ROW_NUMBER):
            resultBoard.append(['W'] * self.n_cols)

        for i in range(self.n_rows - 2 * self.PLAYER_ROW_NUMBER):
            resultBoard.append(['E'] * self.n_cols)

        for i in range(self.PLAYER_ROW_NUMBER):
            resultBoard.append(['B'] * self.n_cols)
        return resultBoard

    def getSpecialPiecesPossibleLocations(self, color, i, j, direction):
        piecesPossibleLocations = []
        if j - 1 >= 0 and (i + direction <= self.n_rows - 1) and (i + direction >= 0) and \
                self.board[i + direction][j - 1] != color:
            piecesPossibleLocations.append((i + direction, j - 1))

        if (i + direction <= self.n_rows - 1) and (i + direction >= 0) and \
                self.board[i + direction][j] == 'E':
            piecesPossibleLocations.append((i + direction, j))

        if j + 1 <= self.n_cols - 1 and (i + direction <= self.n_rows - 1) and (i + direction >= 0) and \
                self.board[i + direction][j + 1] != color:
            piecesPossibleLocations.append((i + direction, j + 1))
        return piecesPossibleLocations

    def getPiecePossibeLocations(self, color, i, j):  # i and j are coordinates
        if color == 'W':
            piecesPossibleLocations = self.getSpecialPiecesPossibleLocations(
                color, i, j, 1)
        else:
            piecesPossibleLocations = self.getSpecialPiecesPossibleLocations(
                color, i, j, -1)
        return piecesPossibleLocations

    def getPiecesPossibleLocations(self, color):
        piecesFromCell = []
        piecesToCell = []
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                piecesPossibleLocations = []
                if self.board[i][j] == color:
                    piecesPossibleLocations = self.getPiecePossibeLocations(
                        color, i, j)
                if len(piecesPossibleLocations) > 0:
                    piecesFromCell.append((i, j))
                    piecesToCell.append(piecesPossibleLocations)

        return piecesFromCell, piecesToCell

    def finishedGame(self):
        if self.win('B') or self.win('W'):
            return True
        return False

    def getNumberOfArmy(self, color):
        armyPositions = self.travelOverBoard(color)
        return len(armyPositions)

    def travelOverBoard(self, color):
        result = []
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i][j] == color:
                    result.append((i, j))
        return result

    def changePieceLocation(self, color, from_, to_):
        self.board[from_[0]][from_[1]] = 'E'
        self.board[to_[0]][to_[1]] = color

    def win(self, color):
        if self.getNumberOfArmy(color) == 0:
            return True
        for i in range(self.n_cols):
            if color == 'B':
                if self.board[0][i] == color:
                    return True
            if color == 'W':
                if self.board[self.n_rows - 1][i] == color:
                    return True
        return False
