import math
import random
from KI import KI
from EventManager import EventManager

C = math.sqrt(2)
INF = float('inf')
N = 1000

class Node:

    def __init__(self, parent, game, value=0):
        self.parent = parent
        self._children = None
        self.value = value
        self.simulations = 0
        self.game = game

    @property
    def is_ki_turn(self):
        # FIXME mcts missing
        self.is_ki_turn = self.game.currentPlayer() == self.mcts.player_id

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
        for i in range(node.game.size[0]):
            for j in range(node.game.size[1]):
                vertex = node.game.HexBoard.getVertex(i,j)
                if vertex.player == None:
                    future_game = node.game.copy()
                    future_game.makeMove([j, i])  # TODO: Right order?
                    yield Node(node, future_game)

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
        self.player_id = 2  # TODO: Pass the number of the ki player
        self.root = Node(None, game)
        self.moves = []
        for child in self.root.children:
            self.simulate(child, N=5)
        if len(self.moves) == 0:
            self.explore_tree()
        print("First level Initialized")

    def explore_tree(self):
        # FIXME: Selects the root node (thats why backpropagate fails)
        node = self.select_node()
        # node becomes None if the game is finished at this point
        while node is not None:
            self.simulate(node)
            node.backpropagate()
            print("Explored node: {} simulations, {} avg value".format(node.simulations, node.value / node.simulations))
            node = self.select_node()

    def getMove(self):
        # Called by framework to return the next step
        return None

    def select_node(self):
        # UCT process to decide if a node is expanded or a new node is explored
        node, uct_value = self.root, self.root.uct()
        # Explore the tree until an uncalculated node is found
        while uct_value is not INF:
            children = [(child, child.uct()) for child in node.children]
            if any([x.game.HexBoard.finished() for x in children]):
                return None
            # Expand nodes with a high UCT rank
            children.sort(key=lambda x: x[1], reverse=True)
            node, uct_value = children[0]
        return node

    @staticmethod
    def options(game):
        for i in range(game.size[0]):
            for j in range(game.size[1]):
                vertex = game.HexBoard.getVertex(i,j)
                if vertex.player == None:
                    yield [j, i]

    def simulate(self, node, N=50):
        success_sum = 0
        for _ in range(N):
            callbacks = EventManager.Events["GameFinished"][:]
            callbacks2 = EventManager.Events["MoveFinished"][:]
            EventManager.Events["GameFinished"].clear()
            EventManager.Events["MoveFinished"].clear()
            simulation = node.game.copy()
            EventManager.subscribe("GameFinished", simulation.HexBoard.onGameFinished)
            while not simulation.HexBoard.finished():
                options = list(self.options(simulation))
                assert len(options) > 0, "No options left but not finished"
                move = options[round(random.random() * (len(options) - 1))]
                simulation.makeMove(move)
            EventManager.Events["GameFinished"] = callbacks
            EventManager.Events["MoveFinished"] = callbacks2
            if simulation.HexBoard.winner() == self.player_id:
                success_sum += 1
        node.simulations += N
        node.value += success_sum
