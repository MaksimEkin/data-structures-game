from avl_handler import *
#from avl import AVLTree


def main(): 

	game_state = avlNew(4, 100, debug=True)
	print('=======================================================')
	# ~ for idx in game_state:
		# ~ print(f'idx: {idx}, {game_state[idx]}')
	game_state = avlAction('Delete node0', game_state, debug = True)
	print('=======================================================')
	game_state = avlAction('Delete node0', game_state, debug = True)
	print('=======================================================')
	game_state = avlAction('Delete node1', game_state, debug = True)
	print('=======================================================')
	game_state = avlAction('Insert 33', game_state, debug = True)
	print('=======================================================')	
	
if __name__ == '__main__':
	
	main()
	
