""" Handles AVL tree state """

''' TO-DO
- Rebalancing is currently automatic and handled during insertion/deletion
- Need to specify how to handle duplicate node values (removing with id)
- Search by id
'''
import sys
sys.path.append('../')
from config import *

from avl import TreeNode
from avl import AVLTree
from random import seed
from random import randint
seed(42)  # fixed seed for debugging

class AVLHandler(object):
	
	def __init__(self, difficulty):
		
		self.root = None
		self.tree = None
		self.cap = 100  # node values will be generated on [0, self.cap]
		self.difficulty = 'Easy'  # default to easy
		if difficulty in DIFFICULTY_LEVELS:
			self.difficulty = difficulty
		self.num_nodes = 0
		self.golden = None  # id of golden node
		self.balanced = True  # currently balancing is done in tandem when insert/remove is called
		
		self.__generate_board()  # generate new game board at runtime
		
	
	def __generate_board(self):
		""" generate game board if it doesnt exists """
		if self.tree:
			return;
			
		self.tree = AVLTree()	
		num_nodes = randint(DIFFICULTY_LEVELS[self.difficulty] - 3, 
		                    DIFFICULTY_LEVELS[self.difficulty])
		nodes = [randint(0, self.cap) for i in range(num_nodes)]
		for node in nodes:
			self.addNode(node)
		
		self.golden = randint(0, num_nodes - 1) # randomly choose golden node
		
	
	def addNode(self, key):
		""" add node to tree by value """
		if self.tree.isIn(self.root, key):  # not adding duplicates (FOR NOW)
			return 
		
		self.root = self.tree.insert_node(self.root, key, self.num_nodes)
		self.num_nodes += 1
		
		
	def delNode(self, key):
		""" remove node from tree by value """
		if self.num_nodes <= 0 or not self.tree.isIn(self.root, key):  # can't remove what's not there
			return 
		
		self.root = self.tree.delete_node(self.root, key)
		self.num_nodes -= 1	
			
		
	def get_gamestate(self):
		""" return dictionary with the gamestate """
		out_dict = {}
		out_dict['nodes'] = self.tree.getNewick(self.root)
		out_dict['node_vals'] = self.tree.getVals(self.root)
		out_dict['gold_node'] = self.golden
		out_dict['balanced'] = self.balanced
		return out_dict
