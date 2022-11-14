import copy
import time
import signal

INFINITY = float('inf')


def handler(signum, frame):
    raise TimeoutError


class Result:
    def __init__(self):
        from_cell = None
        to_cell = None


class Agent:
    def __init__(self, color, opponentColor, time=None):
        self.color = color
        self.opponentColor = opponentColor
        self.timeToMove = time

    def move(self, board):
        # todo: you have to implement this agent.
        if(self.timeToMove == None):
            height = 4
            gameTree = MyTree(board, self.color, self.opponentColor, height)
            AlphaBeta.calLeafValues(gameTree, height)
            return AlphaBeta.computeAlphabeta(gameTree)
        else:
            height = 1
            gameTree = MyTree(board, self.color, self.opponentColor, height)
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(self.timeToMove)
            try:
                result = Result()
                AlphaBeta.calNextMove(
                    gameTree, height, self.timeToMove, result)
            except TimeoutError as e:
                return result.from_cell, result.to_cell


class AlphaBeta:
    @staticmethod
    def calNextMove(tree, height, timeToMove, result):
        # iterative deepening
        for h in range(height, 12):
            AlphaBeta.calLeafValues(tree, h)
            result.from_cell, result.to_cell = AlphaBeta.computeAlphabeta(
                tree)  # best_state
            tree.addOneLevelAtBottom()

    @staticmethod
    def calLeafValues(tree, height):
        # evaluation function
        if(height % 2 == 0):
            color = tree.color
            opponentColor = tree.opponentColor
            isMax = True

        else:
            color = tree.opponentColor
            opponentColor = tree.color
            isMax = False

        for leaf in tree.nodes[height]:
            AlphaBeta.calculateEvaluationFunc(leaf, color, opponentColor)
            if(isMax):
                leaf.setUtility(leaf.utility + leaf.height)
            else:
                leaf.setUtility(leaf.utility - leaf.height)

    @staticmethod
    def computeAlphabeta(tree):
        bestVal = -INFINITY
        beta = INFINITY
        bestNode = None
        children = tree.root.children
        for node in children:
            childVal = AlphaBeta.findBestChildMin(tree, node, bestVal, beta)
            if childVal > bestVal:
                bestVal = childVal
                bestNode = node

        return bestNode.getFromCell(), bestNode.getToCell()

    @staticmethod
    def findBestChildMin(tree, node, alpha, beta):
        if node.board.win(tree.color) and node.board.win(tree.opponentColor):
            return 0-node.height
        if node.board.win(tree.color):
            return 12+node.height
        elif node.board.win(tree.opponentColor):
            return -12-node.height

        value = INFINITY
        if(len(node.children) != 0):
            node.children.sort(key=lambda x: x.utility)
        for child in node.children:
            value = min(value, AlphaBeta.findBestChildMax(
                tree, child, alpha, beta))

            if value <= alpha:
                return value

            beta = min(value, beta)

        if(value == INFINITY):
            AlphaBeta.calculateEvaluationFunc(
                node, node.color, node.opponentColor)
        node.setUtility(node.utility - node.height)
        return node.utility

    @staticmethod
    def findBestChildMax(tree, node, alpha, beta):
        if node.board.win(tree.color) and node.board.win(tree.opponentColor):
            return 0+node.height
        if node.board.win(tree.color):
            return 12+node.height
        elif node.board.win(tree.opponentColor):
            return -12-node.height

        value = -INFINITY
        if(len(node.children) != 0):
            node.children.sort(key=lambda x: x.utility, reverse=True)
        for child in node.children:
            value = max(value, AlphaBeta.findBestChildMin(
                tree, child, alpha, beta))

            if value >= beta:
                return value

            alpha = max(value, alpha)

        if(value == -INFINITY):
            AlphaBeta.calculateEvaluationFunc(
                node, node.color, node.opponentColor)
        node.setUtility(node.utility + node.height)
        return node.utility

    @staticmethod
    def calculateEvaluationFunc(node, color, opponentColor):
        colorScore = 12 - node.board.getNumberOfArmy(opponentColor)
        opponentColorScore = 12 - node.board.getNumberOfArmy(color)
        node.setUtility(colorScore - opponentColorScore)


class MyTree:
    def __init__(self, board, color, opponentColor, height):
        self.height = height
        self.board = board
        self.nodes = [[] for i in range(self.height+1)]
        self.seenBefore = set()  # transposition table - bara kol ya faghat har derakht?
        self.root = self.makeNode(0, board)
        self.buildTree(color, opponentColor)
        self.color = color
        self.opponentColor = opponentColor

    def makeNode(self, height, board, from_cell=None, to_cell=None, color='W', opponentColor='B'):
        node = MyNode(from_cell, to_cell, board, color, opponentColor, height)
        if(height > len(self.nodes)-1):
            self.nodes.append([])
            self.height = height
        self.nodes[height].append(node)
        return node

    def buildTree(self, color, opponentColor):
        maxNodes = [self.root]
        minNodes = []
        maxTurn = True
        for i in range(self.height):
            if maxTurn:
                minNodes = self.makeChildrenFor(
                    maxNodes, color, opponentColor, i+1)
                maxTurn = False
            else:
                maxNodes = self.makeChildrenFor(
                    minNodes, opponentColor, color, i+1)
                maxTurn = True

    def makeChildrenFor(self, nodes, color, opponentColor, height):
        resultNodes = []
        for node in nodes:
            if node.board.win(color) or node.board.win(opponentColor):
                AlphaBeta.calculateEvaluationFunc(node, color, opponentColor)
                continue
            else:
                piecesFromCell, piecesToCell = node.board.getPiecesPossibleLocations(
                    color)
                for i in range(len(piecesToCell)):
                    for j in range(len(piecesToCell[i])):
                        newBoard = copy.deepcopy(node.board)
                        newBoard.changePieceLocation(
                            color, piecesFromCell[i], piecesToCell[i][j])

                        childNode = self.makeNode(
                            height, newBoard, piecesFromCell[i], piecesToCell[i][j], opponentColor, color)
                        if(makeSnapshot(newBoard) in self.seenBefore):
                            continue

                        resultNodes.append(childNode)

                        node.setChild(childNode)

        return resultNodes

    def addOneLevelAtBottom(self):
        height = self.height
        isMax = False
        if self.height % 2 == 0:
            isMax = True
        nodes = self.nodes[len(self.nodes)-1]
        if isMax:
            self.makeChildrenFor(
                nodes, self.color, self.opponentColor, height+1)
        else:
            self.makeChildrenFor(
                nodes, self.opponentColor, self.color, height+1)


def makeSnapshot(board):
    snapshot = ""
    for i in range(board.n_rows):
        for j in range(board.n_cols):
            snapshot += board.board[i][j]
    return snapshot


class MyNode:
    def __init__(self, from_cell, to_here_cell, board, color_, opponentColor_, height_):
        self.children = []
        self.utility = 0
        self.from_cell = from_cell
        self.to_here_cell = to_here_cell
        self.board = board
        self.color = color_
        self.opponentColor = opponentColor_
        self.height = height_

    def setChild(self, child):
        self.children.append(child)

    def setUtility(self, utility):
        self.utility = utility

    def getFromCell(self):
        return self.from_cell

    def getToCell(self):
        return self.to_here_cell
