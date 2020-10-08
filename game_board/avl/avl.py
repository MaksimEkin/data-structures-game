""" AVL Tree for CMSC 447 DSG, Fall 2020

This is an AVL tree implementation that was used in the Data Structures
Game for CMSC 447, Fall 2020. The code was adapted from: https://www.programiz.com/dsa/avl-tree
"""

import sys
sys.path.append('../')
from config import *


class TreeNode(object):
    def __init__(self, key, nid):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.nid = nid


class AVLTree(object):
	
	
	def insert_node(self, root, key, nid):
		""" recursively insert new node 
		
		Keyword arguments:
		root -- current node being compared
		key  -- key value being added
		nid  -- node id
		"""  
		
		if not root:  				# base case
			return TreeNode(key, nid)
		elif key < root.key:  		# go left
			root.left = self.insert_node(root.left, key, nid)
		else:  						# go right
			root.right = self.insert_node(root.right, key, nid)
			
		root.height = 1 + max(self.getHeight(root.left), # update height
							  self.getHeight(root.right))
	
		# Update the balance factor and balance the tree
		''' Currently balancing is automatic. We need to discuss how mistakes 
		    in balancing made by the user are handled '''
		#return(self.__rebalance_helper(root))
		balanceFactor = self.getBalance(root)
		if balanceFactor > 1:
			if self.getBalance(root.left) >= 0:
				return self.rightRotate(root)
			else:
				root.left = self.leftRotate(root.left)
				return self.rightRotate(root)
		if balanceFactor < -1:
			if self.getBalance(root.right) <= 0:
				return self.leftRotate(root)
			else:
				root.right = self.rightRotate(root.right)
				return self.leftRotate(root)
		return root  
		
	
	def delete_node(self, root, key):
		""" recursively remove node
		
		Keyword arguments:
		root -- current node being compared
		key -- key value being removed
		"""    
	
		if not root:  			# base case
			return root
			
		elif key < root.key:	# go left
			root.left = self.delete_node(root.left, key)
			
		elif key > root.key:	# go right
			root.right = self.delete_node(root.right, key)
		else:
			if root.left is None:
				temp = root.right
				root = None
				return temp
			elif root.right is None:
				temp = root.left
				root = None
				return temp
			temp = self.getMinNode(root.right)
			root.key = temp.key
			root.right = self.delete_node(root.right,
										  temp.key)
		if root is None:
			return root
			
		root.height = 1 + max(self.getHeight(root.left), # update height
							  self.getHeight(root.right))
	
	
		# Update the balance factor and balance the tree
		''' Currently balancing is automatic. We need to discuss how mistakes 
		    in balancing made by the user are handled '''
		return(self.__rebalance_helper(root))
	
	
	def isIn(self, root, key):
		""" recursively look for  
		
		Keyword arguments:
		root -- current node being compared
		key  -- key value being added
		nid  -- node id
		"""  
		if not root:  							# base case
			return False
		elif key < root.key:  					# go left
			return self.isIn(root.left, key)
		elif key > root.key:					# go right
			return self.isIn(root.right, key)
		else:
			return True							# found
	
	
	def getVals(self, root):
		""" get key vals for each id 
		
		this could be easily updated to points as well
		"""
		out = {}
		out = self.getVals_helper(root, out)
		return out
	
	
	def getVals_helper(self, root, vals):
		""" helper function for getVals """
		
		if root.left:
			self.getVals_helper(root.left, vals)
		if root.right:
			self.getVals_helper(root.right, vals)
		if root.nid not in vals:
			vals[root.nid] = root.key	
		
		return vals
	
	def getNewick(self, root):
		""" get newick string format of tree """
		out = ''
		out = self.getNewick_helper(root, out)
		out = f"{out};"
		return out
	
	
	def getNewick_helper(self, root, newick):
		""" helper function for getNewick """
		if root.left and not root.right:
			newick = f"(,{self.getNewick_helper(root.left, newick)}){root.nid}"
		elif not root.left and root.right:
			newick = f"({self.getNewick_helper(root.right, newick)},){root.nid}"
		elif root.left and root.right:
			newick = f"({self.getNewick_helper(root.right, newick)},{self.getNewick_helper(root.left, newick)}){root.nid}"
		elif not root.left and not root.right:
			newick = f"{root.nid}"
		else:
			pass

		return newick
	
	
	def leftRotate(self, z): 
		""" perform left rotation """
		y = z.right
		T2 = y.left
		y.left = z
		z.right = T2
		z.height = 1 + max(self.getHeight(z.left),
						   self.getHeight(z.right))
		y.height = 1 + max(self.getHeight(y.left),
						   self.getHeight(y.right))
		return y
	
	
	def rightRotate(self, z):
		""" perform right rotation """
		y = z.left
		T3 = y.right
		y.right = z
		z.left = T3
		z.height = 1 + max(self.getHeight(z.left),
						   self.getHeight(z.right))
		y.height = 1 + max(self.getHeight(y.left),
						   self.getHeight(y.right))
		return y
	

	def getHeight(self, root):
		""" get the height of the node """
		if not root:
			return 0
		return root.height
			
	
	def getMinNode(self, root):
		""" find minimum value node """
		if root is None or root.left is None:
			return root
		return self.getMinNode(root.left)
		
	
	def printKeys(self, currPtr, indent, last):
		""" Debug print key values """
		if currPtr != None:
			sys.stdout.write(indent)
			if last:
				sys.stdout.write("R----")
				indent += "     "
			else:
				sys.stdout.write("L----")
				indent += "|    "
			print(currPtr.key)
			self.printKeys(currPtr.left, indent, False)
			self.printKeys(currPtr.right, indent, True)
			
			
	def printIds(self, currPtr, indent, last):
		""" Debug print id values """
		if currPtr != None:
			sys.stdout.write(indent)
			if last:
				sys.stdout.write("R----")
				indent += "     "
			else:
				sys.stdout.write("L----")
				indent += "|    "
			print(currPtr.nid)
			self.printIds(currPtr.left, indent, False)
			self.printIds(currPtr.right, indent, True)
			
			
	def getBalance(self, root):
		""" Get balance factor of the node """
		if not root:
			return 0
		return self.getHeight(root.left) - self.getHeight(root.right)


	def __rebalance_helper(self, root):
		""" Help rebalance the tree """
		balanceFactor = self.getBalance(root)
		
		if balanceFactor > 1:
			if self.getBalance(root.left) >= 0:
				return self.rightRotate(root)
			else:
				root.left = self.leftRotate(root.left)
				return self.rightRotate(root)
		if balanceFactor < -1:
			if self.getBalance(root.right) <= 0:
				return self.leftRotate(root)
			else:
				root.right = self.rightRotate(root.right)
				return self.leftRotate(root)
		return root

	# ~ def preOrder(self, root):  # preorder print
		# ~ if not root:
			# ~ return
		# ~ print("{0} ".format(root.key), end="")
		# ~ self.preOrder(root.left)
		# ~ self.preOrder(root.right)

if __name__ == '__main__':
	
	sys.stderr.write("Cannot call AVL independently\n")
	
