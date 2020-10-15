from avl_handler import *
from datetime import datetime
seed(42)

NUM_CALLS = 1000


def checkForGolden(node_points, nid):
	
	if nid in node_points:
		return True
	else:
		return False


def checkBadStates():
	
	# Apparently there is an issue with golden node generation.
	# This is a sanity check
	
	bad_states = []
	for i in range(NUM_CALLS):
		
		seed(datetime.now())  # im so random
		
		height = randint(3, 12)  # test trees with 9 - 2049 nodes
		state = avlNew(height, 100, debug=False)
		bad = False
		if not checkForGolden(state['node_points'], state['gold_node']):
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
	

def main(): 


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
	ret, bad_states = checkBadStates()
	if ret:
		print("Uh oh, looks likes theres an issue, go check it out")
		
	
if __name__ == '__main__':
	
	main()
	
