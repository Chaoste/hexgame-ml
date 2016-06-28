import math


C = math.sqrt(2)
INF = float('inf')
N = 1000

class Node:

    def __init__(self, parent, mcts, value=0):
        self.parent = parent
        self.mcts = mcts
        self._children = None
        self.value = value
        self.simulations = 0

    def add_children(*child_nodes):
        self._children += child_nodes

    @property
    def children(self):
        if self._children is None:
            self.mcts.expand(self)
        return self._children

    def backpropagation_value(self):
        # pass mean, max, robust max or mix -> for now try mean
        return self.value / self.simulations

    def backpropagate(self, value=None):
        if None:
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
            math.log(self.parent.simulations) / self.simulations))
        return avg_value + confidence


class MonteCarloTreeSearch:

    def __init__(self):
        # Initialize tree with a root node (which parent is None)
        self.root = Node(None, self)
        self.initial_simulation()

    def __call__(self):
        # Called by framework to return the next step
        new_node = self.select_node()
        self.simulate(new_node)
        new_node.backpropagate()
        return None

    def select_node(self):
        # UCT process to decide if a node is expanded or a new node is explored
        node, uct_value = self.root, self.root.uct()
        # explore the tree until an uncalculated node is found
        while uct_value < INF:
            children = [(child, child.uct() for child in node.children]
            children.sort(key=lambda x: x[1], reverse=True)
            node, uct_value = children[0]
        return node

    def expand(self, node):
        # Get all legal actions for this node. Create node object for
        # each action and add it to the tree / childrens of the given node
        # TODO
        pass

    def simulate(self, node):
        # Do N simulations and save their results
        # TODO
        pass
