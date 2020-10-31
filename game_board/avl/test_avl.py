"""
Run: python3 manage.py test game_board.avl.test_avl
Reference: https://docs.djangoproject.com/en/3.1/topics/testing/overview/
"""

from django.test import TestCase
from game_board.avl.avl_handler import AVLHandler
from game_board.avl.avl_handler import avlNew
from game_board.avl.avl_handler import avlAction
from game_board.avl.avl_handler import avlRebalance
from datetime import datetime
from random import randint
from random import seed

### TEST CONSTANTS ###
NUM_CALLS = 1000


class BColors:
    # Colors for printing
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_golden(handler, checkRoot=True):
    """ Check if valid golden node exists in AVL tree """

    state = handler.get_gamestate()
    gold = state['gold_node']
    nodes = state['node_points']

    if checkRoot and handler.root.nid == handler.golden_id:
        return False

    if gold in nodes:
        return True
    else:
        return False


def check_heights(root):
    """ Traverses tree in preorder and verifies height of each node

    Returns true if every node has expect height
    Returns false if atleast one node is incorrect
    """

    if root:
        return (root.height == get_height(root))
        check_height(root.left)
        check_height(root.right)
    return True


def check_balance(root):
    """ Checks if tree is balanced or not

    Returns true if height balanced
    Returns false if height imbalanced
    """
    if root is None:  # base
        return True

    lHeight = get_height(root.left)  # get heights of each subtree
    rHeight = get_height(root.right)

    # allowed differences are 1, -1, 0
    if ((abs(lHeight - rHeight) <= 1) and
            check_balance(root.left) and
            check_balance(root.right)):
        return True

    # if we reach here means tree is not balanced
    return False


def get_height(root):
    """ Get height of a node

    We're going to be skeptical of the height stored in the node and
    verify it for ourselves. Returns the height. 0 if non-existent node
    """
    if root is None:
        return 0
    return max(get_height(root.left), get_height(root.right)) + 1


class AVLNewGeneration(TestCase):
    """ Test the state of the AVL tree upon generation from scratch"""

    def new_handler(self):
        """ create new handler to test """
        seed(datetime.now())  # im so random
        height = randint(3, 12)  # test trees with 9 - 2049 nodes
        handler = AVLHandler.from_scratch(height, 100)
        return handler

    def test_golden_new(self):
        """ make sure new avl is generated with correct golden node """
        successes = 0
        failures = 0
        iterations = NUM_CALLS

        for i in range(iterations):

            handler = self.new_handler()
            ret = check_golden(handler)
            if ret:
                successes += 1
            else:
                failures += 1
                handler.debug_wrapper()

        if failures != 0:
            print('\n=================================================\n')

        self.assertEqual(failures, 0,
                         msg=f'{BColors.FAIL}\n\t[-]\tFrom scratch: Failed to correctly generate golden node! {failures}/{iterations} failures! {BColors.ENDC}')
        print(
            f"{BColors.OKGREEN}\t[+]\tFrom scratch: Validated correct golden node generation in {successes} trees.{BColors.ENDC}")

    def test_height_new(self):
        """ make sure nodes are generated with correct heights in new trees """
        successes = 0
        failures = 0
        iterations = NUM_CALLS

        for i in range(iterations):

            handler = self.new_handler()
            ret = check_heights(handler.root)
            if ret:
                successes += 1
            else:
                failures += 1

        self.assertEqual(failures, 0,
                         msg=f'{BColors.FAIL}\n\t[-]\tFrom scratch: Failed to correctly generate heights! {failures}/{iterations} failures! {BColors.ENDC}')
        print(
            f"{BColors.OKGREEN}\t[+]\tFrom scratch: Validated correct height for all nodes in {successes} trees.{BColors.ENDC}")

    def test_balance_new(self):
        """ make sure new tree balanced upon generation """
        successes = 0
        failures = 0
        iterations = NUM_CALLS

        for i in range(iterations):

            handler = self.new_handler()
            ret = check_balance(handler.root)
            if ret:
                successes += 1
            else:
                failures += 1
                handler.debug_wrapper()

        if failures != 0:
            print('\n=================================================\n')

        self.assertEqual(failures, 0,
                         msg=f'{BColors.FAIL}\n\t[-]\tFrom scratch: Failed to always generate balanced trees! {failures}/{iterations} failures! {BColors.ENDC}')
        print(
            f"{BColors.OKGREEN}\t[+]\tFrom scratch: Validated that all trees all balanced upon generation in {successes} trees.{BColors.ENDC}")


class AVLOldGeneration(TestCase):
    """ Test the state of the AVL tree upon generation from deserialization"""

    def new_handler(self):
        """ create new handler to test """
        seed(datetime.now())  # im so random
        height = randint(3, 12)  # test trees with 9 - 2049 nodes
        scratch = AVLHandler.from_scratch(height, 100)
        state = scratch.get_gamestate()
        handler = AVLHandler.from_graph(state)
        return handler

    def test_golden_old(self):
        """ make sure new avl is generated with correct golden node """
        successes = 0
        failures = 0
        iterations = NUM_CALLS

        for i in range(iterations):

            handler = self.new_handler()
            ret = check_golden(handler)
            if ret:
                successes += 1
            else:
                failures += 1
                handler.debug_wrapper()

        if failures != 0:
            print('\n=================================================\n')

        self.assertEqual(failures, 0,
                         msg=f'{BColors.FAIL}\n\t[-]\tFrom state:   Failed to correctly generate golden node! {failures}/{iterations} failures! {BColors.ENDC}')
        print(
            f"{BColors.OKGREEN}\t[+]\tFrom state:   Validated correct golden node generation in {successes} trees.{BColors.ENDC}")

    def test_height_old(self):
        """ make sure nodes are generated with correct heights in new trees """
        successes = 0
        failures = 0
        iterations = NUM_CALLS

        for i in range(iterations):

            handler = self.new_handler()
            ret = check_heights(handler.root)
            if ret:
                successes += 1
            else:
                failures += 1

        self.assertEqual(failures, 0,
                         msg=f'{BColors.FAIL}\n\t[-]\tFrom state:   Failed to correctly generate heights! {failures}/{iterations} failures! {BColors.ENDC}')
        print(
            f"{BColors.OKGREEN}\t[+]\tFrom state:   Validated correct height for all nodes in {successes} trees.{BColors.ENDC}")

    def test_balance_old(self):
        """ make sure new tree balanced upon generation """
        successes = 0
        failures = 0
        iterations = NUM_CALLS

        for i in range(iterations):

            handler = self.new_handler()
            ret = check_balance(handler.root)
            if ret:
                successes += 1
            else:
                failures += 1
                handler.debug_wrapper()

        if failures != 0:
            print('\n=================================================\n')

        self.assertEqual(failures, 0,
                         msg=f'{BColors.FAIL}\n\t[-]\tFrom state:   Failed to always generate balanced trees! {failures}/{iterations} failures! {BColors.ENDC}')
        print(
            f"{BColors.OKGREEN}\t[+]\tFrom state:   Validated that all trees all balanced upon generation in {successes} trees.{BColors.ENDC}")


class AVLModification(TestCase):
    """ Test the AVL tree after modifying it """

    def new_handler(self):
        """ create new handler to test, modify it a little """
        seed(datetime.now())  # im so random
        height = randint(3, 12)  # test trees with 9 - 2049 nodes
        handler = AVLHandler.from_scratch(height, 100)

        num_adds = randint(1, height)  # add (1, height) nodes
        num_dels = randint(1, height)  # del (1, height) nodes

        for i in range(num_adds):
            key = randint(1, 100)
            handler.addNewNode(key, b=False)
        for i in range(num_dels):
            nid = randint(0, handler.uid)
            handler.delNodeByID(nid, b=False)

        return handler

    def test_golden_mod(self):
        """ make sure avl still has golden node """
        successes = 0
        failures = 0
        iterations = NUM_CALLS

        for i in range(iterations):

            handler = self.new_handler()
            ret = check_golden(handler, False)  # dont care if root is golden
            if ret:
                successes += 1
            else:
                failures += 1
                handler.debug_wrapper()

        if failures != 0:
            print('\n=================================================\n')

        self.assertEqual(failures, 0,
                         msg=f'{BColors.FAIL}\n\t[-]\tModification: Failed to keep golden node! {failures}/{iterations} failures! {BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tModification: Validated golden node in {successes} trees.{BColors.ENDC}")

    def test_height_mod(self):
        """ make sure node heights are updated with changes """
        successes = 0
        failures = 0
        iterations = NUM_CALLS

        for i in range(iterations):

            handler = self.new_handler()
            ret = check_heights(handler.root)
            if ret:
                successes += 1
            else:
                failures += 1

        self.assertEqual(failures, 0,
                         msg=f'{BColors.FAIL}\n\t[-]\tModification: Failed to correctly modify heights! {failures}/{iterations} failures! {BColors.ENDC}')
        print(
            f"{BColors.OKGREEN}\t[+]\tModification: Validated height adjustment for all nodes in {successes} trees.{BColors.ENDC}")

    def test_balance_mod(self):
        """ make sure balance stored in state is updated with changes correctly """
        successes = 0
        failures = 0
        iterations = NUM_CALLS

        for i in range(iterations):

            handler = self.new_handler()
            ret = check_balance(handler.root)
            if ret == handler.balanced:
                successes += 1
            else:
                failures += 1
                handler.debug_wrapper()

        if failures != 0:
            print('\n=================================================\n')

        self.assertEqual(failures, 0,
                         msg=f'{BColors.FAIL}\n\t[-]\tModification: Failed to modify balance factor correctly! {failures}/{iterations} failures! {BColors.ENDC}')
        print(
            f"{BColors.OKGREEN}\t[+]\tModification: Validated that balance bool is updated in {successes} trees.{BColors.ENDC}")

    def test_rebalance(self):
        """ make sure tree will rebalance when built from graph """
        successes = 0
        failures = 0
        iterations = NUM_CALLS

        for i in range(iterations):

            handler = self.new_handler()
            state = handler.get_gamestate()
            rebal_handler = AVLHandler.from_graph(state)
            ret = check_balance(rebal_handler.root)
            if (ret == True and ret == rebal_handler.balanced):
                successes += 1
            else:
                failures += 1

        self.assertEqual(failures, 0,
                         msg=f'{BColors.FAIL}\n\t[-]\tModification: Failed to correctly rebalance deserialized tree! {failures}/{iterations} failures! {BColors.ENDC}')
        print(
            f"{BColors.OKGREEN}\t[+]\tModification: Validated deserialization rebalancing in {successes} trees.{BColors.ENDC}")
