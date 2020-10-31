""" AVL Tree for CMSC 447 DSG, Fall 2020

This is an AVL tree implementation that was used in the Data Structures
Game for CMSC 447, Fall 2020. The code was adapted from: https://www.programiz.com/dsa/avl-tree
"""

import sys

class TreeNode(object):
    def __init__(self, key, nid):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.nid = nid


class AVLTree(object):
    def insert_node(self, root, key, nid, balance=True):
        """ recursively insert new node

        Keyword arguments:
        root -- current node being compared
        key  -- key value being added
        nid  -- node id
        """
        if not root:  # base case
            return TreeNode(key, nid)
        elif key < root.key:  # go left
            root.left = self.insert_node(root.left, key, nid, balance)
        else:  # go right
            root.right = self.insert_node(root.right, key, nid, balance)

        root.height = 1 + max(self.getHeight(root.left),  # update height
                              self.getHeight(root.right))

        if balance:
            return (self.rebalance(root))
        else:
            return root

    def delete_node(self, root, key, balance=True):
        """ recursively remove node

        Keyword arguments:
        root -- current node being compared
        key -- key value being removed
        """

        if not root:  # base case
            return root

        elif key < root.key:  # go left
            root.left = self.delete_node(root.left, key, balance)

        elif key > root.key:  # go right
            root.right = self.delete_node(root.right, key, balance)
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
            root.right = self.delete_node(root.right, temp.key, balance)
        if root is None:
            return root

        root.height = 1 + max(self.getHeight(root.left),  # update height
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        if balance:
            return (self.rebalance(root))
        else:
            return root

    def delete_node_id(self, root, nid, balance=True):
        """ recursively remove node by id

        Keyword arguments:
        root -- current node being compared
        id -- id of node being removed
        """

        if root and root.nid != nid:
            if root.left and not root.right:  # go left only
                root.left = self.delete_node_id(root.left, nid, balance)
            elif not root.left and root.right:  # go left only
                root.right = self.delete_node_id(root.right, nid, balance)
            elif root.left and root.right:  # do both
                root.left = self.delete_node_id(root.left, nid, balance)
                root.right = self.delete_node_id(root.right, nid, balance)
            else:  # do neither
                return root

        elif not root:
            return root

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
            root.nid = temp.nid
            root.right = self.delete_node_id(root.right, temp.nid, balance)
        if root is None:
            return root

        root.height = 1 + max(self.getHeight(root.left),  # update height
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        if balance:
            return (self.rebalance(root))
        else:
            return root

    def isIn(self, root, key):
        """ recursively look for

        Keyword arguments:
        root -- current node being compared
        key  -- key value being added
        """
        if not root:  # base case
            return False
        elif key < root.key:  # go left
            return self.isIn(root.left, key)
        elif key > root.key:  # go right
            return self.isIn(root.right, key)
        else:
            return True  # found

    def getKeys(self, root):
        """ get keys for each id  """
        keys = {}
        keys = self.__getKeys_helper(root, keys)
        return keys

    def __getKeys_helper(self, root, keys):
        """ helper function for getKeys """

        if root.left:
            self.__getKeys_helper(root.left, keys)
        if root.right:
            self.__getKeys_helper(root.right, keys)
        if root.nid not in keys:
            keys['node' + str(root.nid)] = root.key

        return keys

    def getAdjList(self, root):
        """ create adjacency list from the nodes in the tree

        Adjacency list will be in the form of dict of lists
        First dict is the global adjacency list
        List will contain all adjacent node ids(max 2 for AVL)
        """
        adj = {}
        adj = self.getAdjList_helper(root, adj)
        return adj

    def getAdjList_helper(self, root, adj):
        """ helper function for getVals """

        if root:
            adj['node' + str(root.nid)] = []

            if root.left and not root.right:
                self.getAdjList_helper(root.left, adj)
                adj['node' + str(root.nid)].append('node' + str(root.left.nid))
            elif not root.left and root.right:
                self.getAdjList_helper(root.right, adj)
                adj['node' + str(root.nid)].append('node' + str(root.right.nid))
            elif root.left and root.right:
                self.getAdjList_helper(root.left, adj)
                self.getAdjList_helper(root.right, adj)
                adj['node' + str(root.nid)].append('node' + str(root.left.nid))
                adj['node' + str(root.nid)].append('node' + str(root.right.nid))
            else:
                return

            return adj

        else:
            return

    # DEPRECATED METHOD - USE ADJACENCY LIST
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

    def isBalanced(self, root):
        """ Check if tree is balanced """
        if root is None:
            return True

        fac = abs(self.getBalance(root))
        if (fac <= 1 and
                self.isBalanced(root.left) and
                self.isBalanced(root.right)):
            return True

        return False

    def rebalance(self, root):
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


if __name__ == '__main__':
    sys.stderr.write("Cannot call AVL independently\n")
