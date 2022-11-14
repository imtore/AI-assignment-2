import pygame


class GraphicalBoard:
    def __init__(self, board):
        pygame.init()

        self.SQUARE_SIZE = 90
        self.SQUARE_CENTER = int(-(self.SQUARE_SIZE/2))
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BROWN = (130, 86, 42)

        self.size = (board.n_rows * self.SQUARE_SIZE, board.n_rows * self.SQUARE_SIZE)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Breakthrough Game")

        self.board = board
        self.showBoard()

    def drawLines(self):
        self.screen.fill(self.BROWN)
        for i in range(1, self.board.n_rows):
            pygame.draw.line(self.screen, self.BLACK,
                             (0, i*self.SQUARE_SIZE), (self.SQUARE_SIZE*self.board.n_rows, i*self.SQUARE_SIZE))
            pygame.draw.line(self.screen, self.BLACK,
                             (i*self.SQUARE_SIZE, 0), (i*self.SQUARE_SIZE, self.SQUARE_SIZE*self.board.n_cols))

    def showColorPiece(self, color, blackPiece):
        pygame.draw.circle(self.screen, color,
                           (blackPiece[1] * self.SQUARE_SIZE - self.SQUARE_CENTER,
                            (self.board.n_cols-blackPiece[0]-1) * self.SQUARE_SIZE - self.SQUARE_CENTER),
                           27)

    def showPieces(self):
        blackPiecesLocation = self.board.travelOverBoard('B')
        whitePiecesLocation = self.board.travelOverBoard('W')
        for blackPiece in blackPiecesLocation:
            self.showColorPiece(self.BLACK, blackPiece)
        for whitePiece in whitePiecesLocation:
            self.showColorPiece(self.WHITE, whitePiece)

    def showBoard(self):
        self.drawLines()
        self.showPieces()
        pygame.display.update()
