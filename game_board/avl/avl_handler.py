""" Handles AVL tree state """

import re
from random import seed
from random import choice
from random import randint
from .avl import AVLTree


seed(42)  # fixed seed for debugging


def tryint(s):
    """ try casting s to an int. if exception occurs, return s unchanged """
    try:
        return int(s)
    except ValueError:
        return s


def alphanum_key(s):
    """ Turn string into a list of strings and numbers

    "node20test" --> ["node", 20, "test"]
    """
    return [tryint(c) for c in re.split('([0-9]+)', s)]


class AVLHandler():
    """ Mediary between AVL and API"""
    def __init__(self):
        self.root = None
        self.tree = None
        self.uid = None  # unique id tracker
        self.golden_id = None  # id of golden node
        self.point_cap = None
        self.expected_height = None
        self.balanced = True

    @classmethod
    def from_scratch(cls, expected_height, point_cap):
        """ create new AVL tree with random insertions """
        if expected_height <= 1:
            raise Exception(f"Argument 'expected_height' given invalid value: {expected_height} Must be >1")
        if point_cap <= 2:
            raise Exception(f"Argument 'point_cap' given invalid value: {point_cap} Must be >2")

        handler = cls()
        handler.uid = 0
        handler.golden_id = None  # id of golden node
        handler.point_cap = point_cap
        handler.expected_height = expected_height
        handler.generate_board()  # generate new game board at runtime
        return handler

    @classmethod
    def from_graph(cls, graph):
        """ deserialize existing tree from adjacency list """
        # verify graph has correct keys
        expected_keys = ['adjacency_list', 'node_points', 'gold_node',
                         'root_node', 'balanced', 'uid']
        for key in expected_keys:
            if key not in graph:
                raise Exception(f'Expected key in graph not found: {key}')

        handler = cls()
        handler.uid = tryint(graph['uid'])
        handler.golden_id = tryint(graph['gold_node'][4:])  # remove 'node' from id
        handler.balanced = graph['balanced']
        handler.parse_graph(graph)  # deserialize graph
        return handler

    def generate_board(self):
        """ generate game board if it doesnt exists """
        if self.tree:
            return

        self.tree = AVLTree()
        self.addNewNode(randint(1, self.point_cap))
        while self.root.height < self.expected_height:
            self.addNewNode(randint(1, self.point_cap))

        allUIDs = list(range(self.uid))  # randomly choose golden node
        allUIDs.remove(self.root.nid)
        self.golden_id = choice(allUIDs)

    def parse_graph(self, graph):
        """ deseralize tree from existing tree graph """
        if self.tree:
            return

        self.tree = AVLTree()
        insertion_dict = {}
        nids = graph['adjacency_list']
        keys = graph['node_points']

        for i in nids:
            i_int = i[4:]
            if i_int not in insertion_dict:
                insertion_dict[i_int] = keys[i]

            if len(nids[i]) > 0:  # node has children
                for k in nids[i]:
                    k_int = k[4:]
                    if k_int not in insertion_dict:
                        insertion_dict[k_int] = keys[k]

        for nid in sorted(insertion_dict, key=alphanum_key):
            self.addNode(tryint(insertion_dict[nid]), tryint(nid))

    def addNewNode(self, key, b=True):
        """ add node to tree by value """
        self.root = self.tree.insert_node(self.root, key, self.uid, balance=b)
        self.balanced = self.tree.isBalanced(self.root)
        self.uid += 1

    def addNode(self, key, nid, b=True):
        """ add node to tree by value """
        self.root = self.tree.insert_node(self.root, key, nid, balance=b)
        self.balanced = self.tree.isBalanced(self.root)

    def delNode(self, key, b=True):
        """ remove node from tree by value """
        self.root = self.tree.delete_node(self.root, key, balance=b)
        self.balanced = self.tree.isBalanced(self.root)

    def delNodeByID(self, nid, b=True):
        """ remove node from tree by value """
        if nid != self.golden_id:
            self.root = self.tree.delete_node_id(self.root, nid, balance=b)
            self.balanced = self.tree.isBalanced(self.root)

    def get_gamestate(self):
        """ return dictionary with the gamestate """
        out_dict = {}
        out_dict['adjacency_list'] = self.tree.getAdjList(self.root)
        out_dict['node_points'] = self.tree.getKeys(self.root)
        out_dict['gold_node'] = 'node' + str(self.golden_id)
        out_dict['root_node'] = 'node' + str(self.root.nid)
        out_dict['balanced'] = self.balanced
        out_dict['uid'] = self.uid
        return out_dict

    def debug_print(self, use_id=False):
        """ print tree for debugging """
        if use_id:
            self.tree.printIds(self.root, "", True)
        else:
            self.tree.printKeys(self.root, "", True)

    def debug_wrapper(self):
        """ extra info to be printed for debugging """
        self.debug_print(use_id=False)
        print('\n\nNow with ids. . .')
        self.debug_print(use_id=True)
        print(f'Golden Node:\t{self.golden_id}')
        print(f'Balanced:\t{self.balanced}')
        print(self.tree.getKeys(self.root), '\n')


##### API Callable Functions #####
def avlNew(height, point_cap, debug=False):
    """ create new avl tree of depth with max point value of point_cap """

    handler = AVLHandler.from_scratch(height, point_cap)
    if debug:
        handler.debug_wrapper()
    return handler.get_gamestate()


def avlAction(command, graph, balance=False, debug=False):
    """ take an action on the tree """
    handler = AVLHandler.from_graph(graph)
    c, t = command.split()  # get command and target
    if c == 'Delete':
        nid = tryint(t[4:])
        handler.delNodeByID(nid, b=balance)
        if debug:
            print(f'Tried to delete node of id {nid}')
    elif c == 'Insert':
        key = tryint(t)
        handler.addNewNode(key, b=balance)
        if debug:
            print(f'Tried to add new node with key {key}')
    else:
        raise Exception('Invalid command passed to AVL Handler')

    if debug:
        handler.debug_wrapper()
    return handler.get_gamestate()


def avlRebalance(graph, debug=False):
    """ rebalance graph and return """
    handler = AVLHandler.from_graph(graph)
    if debug:
        handler.debug_wrapper()
    return handler.get_gamestate()
