import {
  default as nodeConfig,
  EMPTY_EDGE_TYPE,
  CUSTOM_EMPTY_TYPE,
  NODE_KEY,
  POLY_TYPE,
  SPECIAL_CHILD_SUBTYPE,
  SPECIAL_EDGE_TYPE,
  SPECIAL_TYPE,
  SKINNY_TYPE
} from "./config";

function create_graph(graph){

	var adjacency_list = graph['adjacency_list'];
	var node_points = graph['node_points'];
	var root_node = graph['root_node'];
	var golden_node = graph['golden_node'];
	const edges = [];
	const nodes = [];
	var node;
	var edge;
	var i;
	var j;
	var label;
	var adjacency_keys = Object.keys(adjacency_list)
	var node_point_keys = Object.keys(node_points)

	// Make the nodes
	for (i = 0; i < adjacency_keys.length; i++) {
		var type = CUSTOM_EMPTY_TYPE
		if  (adjacency_keys[i] == root_node) {
			type = SPECIAL_TYPE;
		}

		node = { id: adjacency_keys[i],
				 title: node_points[adjacency_keys[i]] + " POINTS " + adjacency_keys[i],
				 type: type
		};
		nodes.push(node);

		// Make the edges
		for (j = 0; j < adjacency_list[adjacency_keys[i]].length;j++){

			edge = {handleText: "",
				source: adjacency_keys[i],
				target: adjacency_list[adjacency_keys[i]][j],
				type: SPECIAL_EDGE_TYPE
			};
			edges.push(edge);
		} //for j
		console.log(j);
	}	// for i
	var graph = {"edges": edges,"nodes":nodes};
	return graph;
} // create_graph

function create_adjacency(graph){
var adjacency_list_returnable = {};
var x;
var y;
var node_val;
var count = 0;

for (x = 0; x < graph.nodes.length; x++){
	node_val = graph.nodes[x].id;
	count = 0;
	for(y = 0; y < graph.edges.length; y++ ){
		if (graph.edges[y].source == node_val){
			count += 1;
			if (typeof(adjacency_list_returnable[node_val]) != "undefined"){
				// Adds second Child to array
				adjacency_list_returnable[node_val].push(graph.edges[y].target);
			} else {
				// First Child found, creates the array
				adjacency_list_returnable[node_val] = [graph.edges[y].target];
			} // else
		} // if
		if (count == 2){y = graph.edges.length;}
	} // for
	// Node has no Children
	if (count == 0) adjacency_list_returnable[node_val] = [];
} // for

return adjacency_list_returnable;
} // create_adjacency


export {create_adjacency, create_graph};
