""" Handles AVL tree state """

import re
from avl import TreeNode
from avl import AVLTree
from random import seed
from random import randint
seed(42)  # fixed seed for debugging


def tryint(s):
	try:
		return int(s)
	except ValueError:
		return s
		
def alphanum_key(s):
	""" Turn string into a list of strings and numbers 
	
	"node20test" --> ["node", 20, "test"]
	"""
	return [tryint(c) for c in re.split('([0-9]+)', s)]

class AVLHandler(object):
	
	
	def __init__(self):
		
		self.root = None
		self.tree = None
		
	@classmethod
	def from_scratch(cls, expected_height, point_cap):	
		
		handler = cls()
		handler.num_nodes = 0
		handler.golden_id = None  # id of golden node
		handler.balanced = True  # currently balancing is done in tandem when insert/remove is called
		handler.point_cap = point_cap
		handler.expected_height = expected_height
		handler.__generate_board()  # generate new game board at runtime
		return handler
	
	
	@classmethod
	def from_graph(cls, graph):
		
		handler = cls()
		handler.num_nodes = len(graph['nodes'])
		handler.golden_id = int(graph['gold_node'][4:])  # remove 'node' from id
		handler.balanced = graph['balanced']
		handler.__parse_graph(graph)  # deserialize graph
		return handler
		
	
	def __generate_board(self):
		""" generate game board if it doesnt exists """
		if self.tree:
			return
				
		# ensures that enough unique key values will exist to fill to height				
		val_cap = pow(self.expected_height, 2) * 2 
		self.tree = AVLTree()	
		self.addNewNode(randint(0, val_cap), self.point_cap)
		
		while(self.root.height < self.expected_height):
			self.addNewNode(randint(0, val_cap), self.point_cap)
		
		self.golden_id = randint(0, self.num_nodes - 1) # randomly choose golden node
		
		# fail safe to make sure root is not golden node.
		# if random is seeded with a constant root can be made golden
		timeout = 0
		while(self.root.nid == self.golden_id and timeout < 10):
			self.golden_id = randint(0, self.num_nodes - 1)
			timeout += 1
			
			
	def __parse_graph(self, graph):
		""" deseralize tree from existing tree graph """
		if self.tree:
			return
		
		self.tree = AVLTree()
		insertion_dict = {}
		nodes = graph['nodes']
		root_id = graph['root_node'][4:]  # strip 'node' from id

		for k in nodes:
			if str(k) == root_id:  # root info not in adjacency list, parsed separately
				insertion_dict[root_id] = {'key': graph['node_keys'][graph['root_node']], 
										   'val': graph['node_points'][graph['root_node']]}
								
			if len(nodes[k]) > 0:  # not a null entry
				for i in range(len(nodes[k])):
					nid, mini_dict = self.__parse_graph_helper(nodes[k][i])
					if nid not in insertion_dict:
						insertion_dict[nid] = mini_dict	
			else:
				continue
				
		for nid in sorted(insertion_dict, key=alphanum_key):
			self.addNode(tryint(insertion_dict[nid]['key']), tryint(nid), tryint(insertion_dict[nid]['val']))
	
	
	def __parse_graph_helper(self, entry): 
		""" turn inner node dict into a key and insertion dict """
		
		nid = entry['nid'][4:]  # strip 'node' from id
		out = {'key': entry['key'], 'val': entry['val']}
		return nid, out
		
	
	def addNewNode(self, key, point_cap):
		""" add node to tree by value """
		if self.tree.isIn(self.root, key):  # not adding duplicates 
			return 							# isIn is costly, refactor later
		
		point_val = randint(5, point_cap)
		point_val -= (point_val % 5)  # make all point values divisible by 5
		self.root = self.tree.insert_node(self.root, key, self.num_nodes, point_val)
		self.num_nodes += 1
	
		
	def addNode(self, key, nid, val):
		""" add node to tree by value """
		if self.root and self.tree.isIn(self.root, key):  # not adding duplicates 
			return 										# isIn is costly, refactor later
		
		self.root = self.tree.insert_node(self.root, key, nid, val)
		
		
	def delNode(self, key):
		""" remove node from tree by value """
		if self.num_nodes <= 0 or not self.tree.isIn(self.root, key):  # can't remove what's not there
			return 
		
		self.root = self.tree.delete_node(self.root, key)
		self.num_nodes -= 1
		
		
	def delNodeByID(self, nid):
		""" remove node from tree by value """
		if self.num_nodes <= 0 or not self.tree.isIn(self.root, key):  # can't remove what's not there
			return 
		
		self.root = self.tree.delete_node(self.root, key)
		self.num_nodes -= 1			
			
		
	def get_gamestate(self):
		""" return dictionary with the gamestate """
		out_dict = {}
		out_dict['nodes'] = self.tree.getAdjList(self.root)
		out_dict['node_points'] = self.tree.getVals(self.root)
		out_dict['node_keys'] = self.tree.getKeys(self.root)
		out_dict['gold_node'] = 'node' + str(self.golden_id)
		out_dict['root_node'] = 'node' + str(self.root.nid)
		out_dict['balanced'] = self.balanced
		return out_dict


	def debug_print(self, use_id=False):
		print(f"Tree with {self.num_nodes} nodes. . .")
		if use_id:
			self.tree.printIds(self.root, "", True)
		else:
			self.tree.printKeys(self.root, "", True)
		
		
		
##### API Callable Functions #####
def avlNew(height, point_cap, debug=False):
	""" create new avl tree of depth with max point value of point_cap """
	
	handler = AVLHandler.from_scratch(height, point_cap)
	if debug:
		handler.debug_print(use_id=False)
		print('\n\nNow with ids. . .')
		handler.debug_print(use_id=True)
	return handler.get_gamestate()


def avlAction(command, graph, debug=False):
	""" take an action on the tree """
	
	handler = AVLHandler.from_graph(graph)
	if debug:
		handler.debug_print(use_id=False)
		print('\n\nNow with ids. . .')
		handler.debug_print(use_id=True)
	
	# ~ c,t = command.split()  # get command and target
	# ~ if c == 'Delete':
		# ~ nid = tryint(t[4:])
		# ~ handler.delNode(
	# ~ elif c == 'Insert':
		
	# ~ else:
		# ~ raise Exception('Invalid command passed to AVL Handler')
	
	
def rebalance(graph, debug=False):
	handler = AVLHandler.from_graph(graph)
	return 
	""" rebalance graph and return """
	
	
	
	
