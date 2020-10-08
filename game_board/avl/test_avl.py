from avl_handler import AVLHandler
from avl import AVLTree


def main(): 

	handler = AVLHandler('Hard')
	print(f"Generated Tree. . .")
	handler.tree.printKeys(handler.root, "", True)  # print tree
	
	key = 29
	handler.addNode(key)
	print(f"\nAdded {key}. . .")
	handler.tree.printKeys(handler.root, "", True)  # print tree
	
	key = 28
	print(f"\nRemoved {key}. . .")
	handler.delNode(key)
	handler.tree.printKeys(handler.root, "", True)  # print tree
	
	print(f"\nPrint tree by id values. . .")
	handler.delNode(key)
	handler.tree.printIds(handler.root, "", True)  # print tree

	print()
	graph = handler.get_gamestate()
	for idx in graph:
		print(f"{idx} : {graph[idx]}")
	
if __name__ == '__main__':
	
	main()
	
