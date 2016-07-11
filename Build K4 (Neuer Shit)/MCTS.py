import math
import random
import time
from KI import KI
from EventManager import EventManager

# Decrease to expand a path deeper before exploring other paths
C = math.sqrt(2)
INF = float('inf')
N = 1000

class Node:

    def __init__(self, parent, hexBoard, player, value=0):
        self.parent = parent
        self._children = None
        self.value = value
        self.simulations = 0
        self.hexBoard = hexBoard
        self.player = player

    @property
    def is_ki_turn(self):
        # TODO: Use player_id instead of 2
        return self.hexBoard.currentPlayer() == self.player

    def add_children(*child_nodes):
        self._children += child_nodes

    @property
    def children(self):
        if self._children is None:
            self._children = list(self.expand(self))
        return self._children

    def expand(self, node):
        # Get all legal actions for this node. Create node object for
        # each action and add it to the tree / childrens of the given node
        for i in range(self.hexBoard.size[0]):
            for j in range(self.hexBoard.size[1]):
                vertex = self.hexBoard.getVertex(i,j)
                if vertex.player == None:
                    future_hexBoard = self.hexBoard.copy()
                    future_hexBoard.receiveMove([i, j])
                    yield Node(node, future_hexBoard, self.player)

    def backpropagation_value(self):
        # pass mean, max, robust max or mix -> for now try mean
        return self.value / self.simulations

    def backpropagate(self, value=None):
        if value is None:
            self.parent.backpropagate(self.backpropagation_value())
            return
        self.simulations += 1
        self.value += value
        if self.parent:
            self.parent.backpropagate(value)

    def uct(self):
        if self.simulations == 0:
            return INF
        avg_value = self.value / self.simulations
        confidence = C * math.sqrt(
            math.log(self.parent.simulations) / self.simulations)
        return avg_value + confidence


class MonteCarloTreeSearch(KI):

    def __init__(self, game, player_id):
        super().__init__(game)
        # Initialize tree with a root node (which parent is None)
        self.player_id = player_id  # TODO: Pass the number of the ki player
        self.root = Node(None, game.HexBoard, player_id)
        self.moves = []
        # TODO: Make simulation faster by not copying the whole game object
        print("Exploring the tree")
        start = time.time()
        for child in self.root.children:
            self.simulate(child, N=100)
            child.backpropagate()
        print("First level Initialized - Took:", time.time() - start)
        start = time.time()
        self.explore_tree()
        print("Explored tree - Took:", time.time() - start)


    def explore_tree(self):
        node, _ = self.select_node()
        # node becomes None if the game is finished at this point
        while node is not None:
            self.simulate(node)
            print("Explored node: {} simulations, {} avg value".format(node.simulations, node.value / node.simulations))
            node.backpropagate()
            node, moves = self.select_node()
        # Remove enemy moves (depending on starting player)
        assert self.player_id in (1, 2), "Invalid player_id '{}'".format(self.player_id)
        if self.player_id == 1:
            moves = moves[::2]
        elif self.player_id == 2:
            moves = moves[1::2]
        self.moves = moves

    def receiveMove(self, move):
        # Enemy action -> Because this is not an online version, the MCTS
        # doesn't react on the choice of its enemy. Might raise an Exception
        pass

    def nextMove(self):
        # Called by framework to return the next step
        step = self.Game.moveCounter // 2
        assert step < len(self.moves), 'Calculated solution is too short: ' + str(len(self.moves))
        return self.moves[step]

    def select_node(self):
        # UCT process to decide if a node is expanded or a new node is explored
        node, uct_value = self.root, 0
        # Explore the tree until an uncalculated node is found
        depth = 0
        moves = []
        while uct_value is not INF:
            children = [(child, child.uct()) for child in node.children]
            if any([x.hexBoard.finished() for (x, y) in children]):
                return None, moves
            # Expand nodes with a high UCT rank
            children.sort(key=lambda x: x[1], reverse=True)
            node, uct_value = children[0]
            moves.append(node.hexBoard.lastMove)
            depth += 1
        print("Selected node with depth", depth, "Parent UCT:", node.parent.uct())
        return node, moves

    @staticmethod
    def options(hexBoard):
        for i in range(hexBoard.size[0]):
            for j in range(hexBoard.size[1]):
                vertex = hexBoard.getVertex(i,j)
                if vertex.player == None:
                    yield [i, j]

    def simulate(self, node, N=20):
        success_sum = 0
        for _ in range(N):
            callbacks = EventManager.Events["GameFinished"][:]
            callbacks2 = EventManager.Events["MoveFinished"][:]
            EventManager.Events["GameFinished"].clear()
            EventManager.Events["MoveFinished"].clear()
            simulation = node.hexBoard.copy()
            while not simulation.finished():
                options = list(self.options(simulation))
                assert len(options) > 0, "No options left but not finished"
                move = options[round(random.random() * (len(options) - 1))]
                simulation.receiveMove(move)
            EventManager.Events["GameFinished"] = callbacks
            EventManager.Events["MoveFinished"] = callbacks2
            if simulation.winner() == self.player_id:
                success_sum += 1
        node.simulations += N
        node.value += success_sum
