import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Button, Grid, Typography, Card, CardHeader, CardActions, CardActionArea, CardContent, Chip } from '@material-ui/core';
import {create_adjacency, create_graph} from './CreateGraphAdj.js';
import Cookies from 'universal-cookie';


//Uber's digraph react folder

import {
  GraphView, // required
  LayoutEngineType,
} from "react-digraph";

import {
  default as nodeConfig,
  EMPTY_EDGE_TYPE,
  CUSTOM_EMPTY_TYPE,
  NODE_KEY,
  POLY_TYPE,
  SPECIAL_CHILD_SUBTYPE,
  SPECIAL_EDGE_TYPE,
  SPECIAL_TYPE,
  SKINNY_TYPE,
    GOLD_NODE
} from "./config";

import "./styles.css";

//Fix XSS security issues when developing locally
//this allows us to test separately locally and on Heroku by changing just one line
const local = "http://127.0.0.1:8000/";
const reactLocal = "http://localhost:3000/"
const remote = "https://data-structures-game.herokuapp.com/";

//can also be const url = local; or const url = reactLocal;
const url = remote;

const sample = {
  edges: [{}],
  nodes: [{ id: "start1", title: "Start (0)", type: GOLD_NODE,  node_id:"", points:0 },]
};

//Gameboard Component
class GameBoard extends Component {
  constructor(props) {
    super(props);
    //this is used for accessing variables between components
    this.customNodeRef = React.createRef();


    //state of the board
    this.state = {
      graph: sample,
      selected: {},
      layoutEngineType: 'VerticalTree',

      addModalClose:false,
      addModalShow:false,

      loading: true,

      //store state of board
      board: null,
      gameID: null,
      turn: null,
      playerCardChoice: null,
      playerBalanceAttempt: null,
      difficulty:null,
      players:null,
      data_structure:null
    };
  }
  // Initialize component objects by setting state and props of the gameboard
  // Before compoenentDidMount is called the render menthod is called to
  // access the DOM to make API calls and update the state and re-renders
  // component did mount to update the values of the state

  async componentDidMount() {
        const cookies = new Cookies();
        //set state varibals to these variables to be used in the url
        let difficulty = cookies.get('level');
        let players = cookies.get('playerList');
        let ds = cookies.get('gameDS');

       //get cookie variables from state and insert into url
       let createGameURL = url+"game_board/api/start_game/" + difficulty + "/" + players + "/" + ds
       let getGameURL = url+"game_board/api/board/";

       //get request to get game id
       let response = await fetch(createGameURL);
       let game_id = await response.json();
      //save the get request response to state
       this.setState({ gameID: game_id['game_id']});
       cookies.set('game_id', game_id['game_id'], { path: '/' });

       //get request to api and include the dynamic game_id

       response = await fetch(getGameURL + game_id['game_id']);
       let board_ = await response.json();
       //set the state values with respect to the dynamic json response
       this.setState({ board: board_, loading: false, turn: board_['turn']});

        //pass the new board state into create_graph function and 
        //set the made_graph state
       let made_graph = create_graph(this.state.board['graph'])
       this.setState({ graph: made_graph});
    }

    //from imported digraph folder
  renderNode = (nodeRef, data, id, selected, hovered) => {
    return (
      <g x="0" y="0" className={`shape`}>
        {!selected ? null : (
          <foreignObject
            style={{ pointerEvents: "all" }}
            width="100"
            height="50"
            xmlnsXlink="http://www.w3.org/1999/xlink"
          >
          </foreignObject>
        )}
        <use
          className={`node ${hovered ? "hovered" : ""} ${
            selected ? "selected" : ""
          }`}
          x="-77"
          y="-77"
          width="154"
          height="154"
          xlinkHref={`#${data.type}`}
        >
          <svg viewBox="-27 0 154 154" id={data.type} width="154" height="154">
            <rect
              transform="translate(50) rotate(45)"
              width="109"
              height="109"
            />
          </svg>
        </use>
      </g>
    );
  };



  //from imported digraph folder
  //uncommented for later use

  //may need later
  // onSelectEdge = (node, event) => {
  //   //console.log("test select edge");
  // };

  // onUpdateNode = () => true;

  // onDeleteNode = (...args) => {
  //   this.setState({});
  // };

  //returns index of a specified node

  getNodeIndex(searchNode) {
    return this.state.graph.nodes.findIndex(node => {
      return node[NODE_KEY] === searchNode[NODE_KEY];
    });
  }

  //from imported digraph folder
  // Helper to find the index of a given edge
  getEdgeIndex(searchEdge) {
    return this.state.graph.edges.findIndex(edge => {
      return (
        edge.source === searchEdge.source && edge.target === searchEdge.target
      );
    });
  }

  //from imported digraph folder
  // Given a nodeKey, return the corresponding node
  getViewNode(nodeKey) {
    const searchNode = {};

    searchNode[NODE_KEY] = nodeKey;
    const i = this.getNodeIndex(searchNode);

    return this.state.graph.nodes[i];
  }


  //from imported digraph folder
  //board always has start node

  addStartNode = e => {
    const graph = this.state.graph;

    // using a new array like this creates a new memory reference
    // this will force a re-render
    graph.nodes = [
      {
        id: Date.now(),
        title: "Node A",
        type: SPECIAL_TYPE,
        x: e ? e.screenX : 0, //Figure out the correct coordinates to drop
        y: e ? e.screenY : 0
      },
      ...this.state.graph.nodes
    ];
    this.setState({
      graph
    });
  };

  //from imported digraph folder
  //delete header node
  deleteStartNode = () => {
    const graph = this.state.graph;

    graph.nodes.splice(0, 1);
    // using a new array like this creates a new memory reference
    // this will force a re-render
    graph.nodes = [...this.state.graph.nodes];
    this.setState({
      graph
    });
  };

    //from imported digraph folder
  handleChange = event => {
    this.setState(
      {
        totalNodes: parseInt(event.target.value || "0", 10)
      },
      this.makeItLarge
    );
  };

  //from imported digraph folder
  //Handlers/Interaction
  // Called by 'drag' handler, etc..
  // to sync updates from D3 with the graph
  onUpdateNode = viewNode => {
    const graph = this.state.graph;
    const i = this.getNodeIndex(viewNode);

    graph.nodes[i] = viewNode;
    this.setState({ graph });
  };

    //from imported digraph folder
  // Node 'mouseUp' handler
  onSelectNode = (viewNode, event) => {
    const { id = "" } = event.target;
    if (id.includes("text")) {
      document.getElementById(event.target.id).click();
    }

    //from imported digraph folder
    // Deselect events will send Null viewNode
    this.setState({ selected: viewNode });
  };

    //from imported digraph folder
  // Edge 'mouseUp' handler
  onSelectEdge = viewEdge => {
    this.setState({ selected: viewEdge });
  };

    //from imported digraph folder
  // Updates the graph with a new node
  onCreateNode = (x, y) => {
    const graph = this.state.graph;

    //from imported digraph folder
    // This is just an example - any sort of logic
    // could be used here to determine node type
    // There is also support for subtypes. (see 'sample' above)
    // The subtype geometry will underlay the 'type' geometry for a node
    const type = Math.random() < 0.25 ? SPECIAL_TYPE : CUSTOM_EMPTY_TYPE;

    const viewNode = {
      id: Date.now(),
      title: "",
      node_id:"",
      points:0,
      type,
      x,
      y
    };

    graph.nodes = [...graph.nodes, viewNode];
    this.setState({ graph });
  };

    //from imported digraph folder
  // Deletes a node from the graph
  onDeleteNode = (viewNode, nodeId, nodeArr) => {
    const graph = this.state.graph;
    // Delete any connected edges
    const newEdges = graph.edges.filter((edge, i) => {
      return (
        edge.source !== viewNode[NODE_KEY] && edge.target !== viewNode[NODE_KEY]
      );
    });

    graph.nodes = nodeArr;
    graph.edges = newEdges;

    this.setState({ graph, selected: null });
  };

    //from imported digraph folder
  // Creates a new node between two edges
  onCreateEdge = (sourceViewNode, targetViewNode) => {
    const graph = this.state.graph;
    // This is just an example - any sort of logic
    // could be used here to determine edge type
    const type =
      sourceViewNode.type === SPECIAL_TYPE
        ? SPECIAL_EDGE_TYPE
        : EMPTY_EDGE_TYPE;

    const viewEdge = {
      source: sourceViewNode[NODE_KEY],
      target: targetViewNode[NODE_KEY],
      type
    };

    //from imported digraph folder
    // Only add the edge when the source node is not the same as the target
    if (viewEdge.source !== viewEdge.target) {
      graph.edges = [...graph.edges, viewEdge];
      this.setState({
        graph,
        selected: viewEdge
      });
    }
  };

  // Called when an edge is reattached to a different target.
  onSwapEdge = (sourceViewNode, targetViewNode, viewEdge) => {
    const graph = this.state.graph;
    const i = this.getEdgeIndex(viewEdge);
    const edge = JSON.parse(JSON.stringify(graph.edges[i]));

    edge.source = sourceViewNode[NODE_KEY];
    edge.target = targetViewNode[NODE_KEY];
    graph.edges[i] = edge;
    // reassign the array reference if you want the graph to re-render a swapped edge
    graph.edges = [...graph.edges];

    this.setState({
      graph,
      selected: edge
    });
  };

  // Called when an edge is deleted
  onDeleteEdge = (viewEdge, edges) => {
    const graph = this.state.graph;

    graph.edges = edges;
    this.setState({
      graph,
      selected: null
    });
  };

    //from imported digraph folder
  onUndo = () => {
    console.warn("Undo is not currently implemented in the example.");
    // Normally any add, remove, or update would record the action in an array.
    // In order to undo it one would simply call the inverse of the action performed. For instance, if someone
    // called onDeleteEdge with (viewEdge, i, edges) then an undelete would be a splicing the original viewEdge
    // into the edges array at position i.
  };


    //from imported digraph folder
  //functions for copying and pasting nodes from tree
  onCopySelected = () => {
    if (this.state.selected.source) {
      console.warn("Cannot copy selected edges, try selecting a node instead.");

      return;
    }

    const x = this.state.selected.x + 10;
    const y = this.state.selected.y + 10;

    this.setState({
      copiedNode: { ...this.state.selected, x, y }
    });
  };
 
    //from imported digraph folder 
  onPasteSelected = () => {
    if (!this.state.copiedNode) {
      console.warn(
        "No node is currently in the copy queue. Try selecting a node and copying it with Ctrl/Command-C"
      );
    }

    const graph = this.state.graph;
    const newNode = { ...this.state.copiedNode, id: Date.now() };

    graph.nodes = [...graph.nodes, newNode];
    this.forceUpdate();
  };

    //from imported digraph folder
  handleChangeLayoutEngineType = event => {
    this.setState({
      layoutEngineType: event.target.value
    });
  };

    //from imported digraph folder
  onSelectPanNode = event => {
    if (this.GraphView) {
      this.GraphView.panToNode(event.target.value, true);
    }
  };

  /* Define custom graph editing methods here */

  // arg: card chosen
  // call action api which returns new board
  // sets the new board

  //for playing first card (one displayed on far left)
  playCard = (card) => {
    const cookies = new Cookies();
    cookies.set('selectedCard', card, { path: '/' });
    this.apiCall()
  }

  apiCall = async () => {
    const cookies = new Cookies();
    let selectedCard = cookies.get('selectedCard');
    let fetch_url = url+"game_board/api/action/" + selectedCard + '/'

    fetch_url = fetch_url + this.state.board['game_id']

    this.setState({ loading: true});

    let response = await fetch(fetch_url);
    let newBoard = await response.json();
    this.setState({ board: newBoard, loading: false, turn: newBoard['turn']});

    let made_graph = create_graph(this.state.board['graph'])
    this.setState({ graph: made_graph});

  }

  // Create custom text content for the nodes: Node point and Node ID
  renderNodeText = (data) => {
    console.log(data);
    return (
      <foreignObject x='-20' y='-30' width='200' height='50'>
        <div className="graph_node">
          <p className="node_points_text">{data.points}</p>
          <p className="node_id_text">{data.node_id}</p>
        </div>
      </foreignObject>
    );
  };


  //in react life cycle, code that is rendered occurs after constructor initialization
  //and component mounting and then reflects the change in state/prop values
  //then it checks if the change needs to be re-rendered

  render() {

    //statically store this.state

    const nodes = this.state.graph.nodes;
    const edges = this.state.graph.edges;
    const selected = this.state.selected;

    //variables to store cards
    let card_1 = null;
    let card_2 = null;
    let card_3 = null;

    //if loading is completed, statically store cards
    if (!this.state.loading) {


      // get the value of api json return index 0,1,2

      // here staticly getting the cards so change, plus it would have to be updateding as we play
      card_1 = this.state.board['cards'][this.state.board['turn']][0]
      card_2 = this.state.board['cards'][this.state.board['turn']][1]
      card_3 = this.state.board['cards'][this.state.board['turn']][2]
    }

    //html returned to display page. When each card is played, the appropriate function is called, which in turn makes an API call

    return (

      //format code to display the 3 cards in flex boxes
      <div>
        <div> {this.state.difficulty}</div>

        <div style={{height: "10rem"}}>
          <div className="text-center text-6xl font-bold"> It's {this.state.turn }'s turn! </div>

          <div className="bg-gray-200 flex items-center bg-gray-200 h-10">

            <div className="flex-1 text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
              <button onClick={() => this.playCard(card_1)}>{card_1}</button>
            </div>

            <div className="flex-1 text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
              <button onClick={() => this.playCard(card_2)}>{card_2}</button>
            </div>

            <div className="flex-1 text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
              <button onClick={() => this.playCard(card_3)}>{card_3}</button>
            </div>
          </div>

        {/*from react digraph library to format graph */}
        <div id = "graph" style={{ height: "60rem"}}>
          <GraphView
          showGraphControls={true}
          gridSize="100rem"
          gridDotSize={1}
          renderNodeText={this.renderNodeText}
          ref="GraphView"
          nodeKey={NODE_KEY}
          nodes={nodes}
          edges={edges}
          selected={selected}
          nodeTypes={nodeConfig.NodeTypes}
          nodeSubtypes={nodeConfig.NodeSubtypes}
          edgeTypes={nodeConfig.NodeTypes}
          onSelectNode={this.onSelectNode}
          onCreateNode={this.onCreateNode}
          onUpdateNode={this.onUpdateNode}
          onDeleteNode={this.onDeleteNode}
          onSelectEdge={this.onSelectEdge}
          onCreateEdge={this.onCreateEdge}
          onSwapEdge={this.onSwapEdge}
          onDeleteEdge={this.onDeleteEdge}
          readOnly={false}
          dark={true}
          layoutEngineType={this.state.layoutEngineType}
        />
        </div>

      </div>
      </div>
    );
  }
}
export default GameBoard;
const rootElement = document.getElementById("root");
ReactDOM.render(<GameBoard />, rootElement);


