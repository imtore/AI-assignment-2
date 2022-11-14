import math


class Minimax:
    @staticmethod
    def calNextMove(tree, height):
        Minimax.computeEvaluationFunction(tree, height)
        Minimax.computeMinimaxValueNodes(tree, height)
        decistionNode = tree.root.getDecisionChild()
        return decistionNode.getFromCell(), decistionNode.getToCell()

    @staticmethod
    def computeMinimaxValueNodes(tree, height):
        isMax = True
        if height % 2 == 0:
            isMax = False
        for i in range(height, 0, -1):
            if not isMax:
                Minimax.chooseDecistionChild(False, i-1, math.inf, tree)
                isMax = True
            else:
                Minimax.chooseDecistionChild(True, i-1, -math.inf, tree)
                isMax = False

    @staticmethod
    def chooseDecistionChild(isMax, i, maxMinValue, tree):
        for j in range(len(tree.nodes[i])):
            father = tree.nodes[i][j]
            maxMinUtility = maxMinValue
            decisionNode = None
            if len(father.children) > 0:
                for child in father.children:
                    if not isMax:
                        if child.utility < maxMinUtility:
                            maxMinUtility = child.utility
                            decisionNode = child
                    if isMax:
                        if child.utility > maxMinUtility:
                            maxMinUtility = child.utility
                            decisionNode = child
                father.setUtility(maxMinUtility)
                father.setDecisionChild(decisionNode)

    @staticmethod
    def computeEvaluationFunction(tree, height):
        for leaf in tree.nodes[height]:
            leaf.setEvaluationFunction()
