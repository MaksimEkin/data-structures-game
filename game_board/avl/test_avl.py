"""
Run: python3 manage.py test game_board.avl.test_avl
Refrence: https://www.django-rest-framework.org/api-guide/testing/
"""

from django.test import TestCase
from rest_framework.test import APIClient
from game_board.avl.avl_handler import avlNew
from game_board.avl.avl_handler import avlAction
from game_board.avl.avl_handler import avlRebalance
from datetime import datetime
from random import randint
from random import seed

seed(42)
NUM_CALLS = 1000


class AVLOverview(TestCase):
	
	def checkForGolden(self, node_points, nid):	
		if nid in node_points:
			return True
		else:
			return False

	
	def checkBadStates(self):

		bad_states = []
		for i in range(NUM_CALLS):
			
			seed(datetime.now())  # im so random
			
			height = randint(3, 12)  # test trees with 9 - 2049 nodes
			state = avlNew(height, 100, debug=False)
			bad = False
			if not self.checkForGolden(state['node_points'], state['gold_node']):
				bad = True
			if not state['balanced']:
				bad = True
			if bad:
				print(f'({i})\t Found bad state')
				bad_states.append(state)
			
			
		if bad_states:
			return True, bad_states
		else:
			return False, None
		
	
	def test_bad_state_generation(self):
		""" Test valid tree generation """
	
		# Manual Analysis
		game_state = avlNew(3, 100, debug=True)
		print('=======================================================')
		game_state = avlAction('Delete node0', game_state, debug = True)
		print('=======================================================')
		game_state = avlAction('Delete node0', game_state, debug = True)
		print('=======================================================')
		game_state = avlAction('Delete node1', game_state, debug = True)
		print('=======================================================')
		game_state = avlAction('Insert 94', game_state, debug = True)
		print('=======================================================')
		game_state = avlRebalance(game_state, debug = True)
		
		# break state, check if it still works
		del game_state['node_points']
		try:
			game_state = avlRebalance(game_state, debug = True)
		except Exception as e:
			print("This should have thrown exception. Printing exception:")
			print(e)
		
		# Random Testing
		ret, bad_states = self.checkBadStates()
		if ret:
			print("Uh oh, looks likes theres an issue, go check it out")
			
		
		print('Finished!')
