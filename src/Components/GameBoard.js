import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Button, Grid, Typography, Card, CardHeader, CardActions, CardActionArea, CardContent, Chip } from '@material-ui/core';
import {create_adjacency, create_graph} from './CreateGraphAdj.js';
import Cookies from 'universal-cookie';
import WinModal from './Modal/WinModal.js';
import ReactTooltip from "react-tooltip";
import Particles from 'react-particles-js';
import Swal from "sweetalert2"

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

//define sample node
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

      read_only:true,

      //waiting on API call?
      loading: true,

      //store state of board
      board: null,
      gameID: null,
      token: "-1",
      username: "-1",
      turn: "",
      deckSize: 1000,
      playerPointVal: null,
      playerCardChoice: null,
      playerBalanceAttempt: null,
      difficulty:null,
      players:null,
      playersArray:[],
      data_structure:null,
      initial_load:true,

      //used in conjunction with the API's end_game returned in the JSON
      game_over: false
    };
    
    
  }

  // Initialize component objects by setting state and props of the gameboard
  // Before compoenentDidMount is called the render method is called to
  // access the DOM to make API calls and update the state and re-renders
  // component did mount to update the values of the state
  async componentDidMount() {

    const cookies = new Cookies();

    //set state variables to these variables to be used in the url
    let difficulty = cookies.get('level');
    let players = cookies.get('playerList');

    if (cookies.get('username') != null && cookies.get('token') != null) {
      if (cookies.get('username') != "" && cookies.get('token') != "") {
        this.setState({ username: cookies.get('username'), token: cookies.get('token') })
        players = players + "," + cookies.get('username');
      }
    }

    this.setState({ playersArray: players.split(',') })
    let ds = cookies.get('gameDS');

    console.log("players: " + players)
    console.log("playersArray: " + this.state.playersArray)

    //get cookie variables from state and insert into url
    let createGameURL = url + "game_board/api/start_game/" + difficulty + "/" + players + "/" + ds
    let getGameURL = url + "game_board/api/board/";


    //API call to start game
    let response = await fetch(createGameURL);
    let game_id = await response.json();

    //save the get request response to state
    this.setState({ gameID: game_id['game_id'] });
    cookies.set('game_id', game_id['game_id'], { path: '/' });

    //get request to api and include the dynamic game_id
    response = await fetch(getGameURL + game_id['game_id']);
    let board_ = await response.json();

    //set the state values with respect to the dynamic json response
    this.setState({ board: board_, turn: board_['turn'] });
    this.setState({ playerPointVal: board_['player_points'][this.state.turn] });
    this.setState({ deckSize: board_['deck'].length });

    //pass the new board state into create_graph function and set the made_graph state
    let made_graph = create_graph(this.state.board['graph'])
    this.setState({ graph: made_graph });
    this.setState({ loading: false, initial_load: false });

    if (!this.state.game_over) {
      if (this.state.turn.replace(/\s+/g, "").toLowerCase().startsWith('bot')) {
        if (!this.state.loading) {
          // if this is a bot, call AI action
          this.aiCall()
        }
      }
    }
  }

  //from imported digraph folder - function to display node
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
  //uncomment for later use

  /*may need later
  onSelectEdge = (node, event) => {
    console.log("test select edge");
  }; */

  // onUpdateNode = () => true;

  /* onDeleteNode = (...args) => {
     this.setState({});
   }; */

  //from imported digraph folder - returns index of a specified node
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
  //Given a nodeKey, return the corresponding node
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

    this.setState({ selected: viewNode });
  };

  //from imported digraph folder
  // Edge 'mouseUp' handler
  onSelectEdge = viewEdge => {
    this.setState({ selected: viewEdge });
  };

  //from imported digraph folder
  //Updates the graph with a new node
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
  //Deletes a node from the graph
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
  //Creates a new node between two edges
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
    //Only add the edge when the source node is not the same as the target
    if (viewEdge.source !== viewEdge.target) {
      graph.edges = [...graph.edges, viewEdge];
      this.setState({
        graph,
        selected: viewEdge
      });
    }
  };

  //Called when an edge is reattached to a different target.
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

  //Called when an edge is deleted
  onDeleteEdge = (viewEdge, edges) => {
    const graph = this.state.graph;

    graph.edges = edges;
    this.setState({
      graph,
      selected: null
    });
  };

  //from imported digraph folder
  //Undo function
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

  //checks if the current board is balanced and returns true or false
  checkRebalance = () => {
    let isBalanced = this.state.board.graph.balanced
    console.log("balanced: ",this.state.board.graph.balanced)
    return isBalanced
  }

  //called if checkRebalance returns false
  //post request to get correct/balanced game board and sets gameboard to
  //return balanced board
  rebalance = async () => {
    this.setState({loading:true})

    let fetch_url = url+"game_board/api/rebalance/" + this.state.gameID + '/' + this.state.username + '/' + this.state.token
    let balance_attempt={'adjacency_list':{'node2':['node0'],'node0':['node5','node3'],'node5':[],'node3':[]}}
    let requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(balance_attempt)
    };
    console.log("request option parameters: ", requestOptions)
    let response = await fetch(fetch_url, requestOptions);
    let newBoard = await response.json();

    //player might lose points when re-balance occurs
    this.setState({playerPointVal: newBoard['player_points'][this.state.turn]})
    this.setState({ board: newBoard, turn: newBoard['turn']});

    let made_graph = create_graph(this.state.board['graph'])
    this.setState({ graph: made_graph});
    this.setState({loading: false})

  }

  // arg: card chosen
  // call action api which returns new board
  // sets the new board
  playCard = (card) => {
    const cookies = new Cookies()
    cookies.set('selectedCard', card, { path: '/' })

    //make the API call to actually play the card the user chose
    this.apiCall()

    //check if playing selected card ended the game
    //this.checkGameStatus()
  }

  //modularize the api call for playing a card
  apiCall = async () => {
    const cookies = new Cookies();

    //form the URL that will be used
    let selectedCard = cookies.get('selectedCard');
    let fetch_url = url+"game_board/api/action/" + selectedCard + '/' + this.state.board['game_id'] + '/' + this.state.username + '/' + this.state.token

    this.setState({ loading: true});

    //make the API call
    let response = await fetch(fetch_url);
    let newBoard = await response.json();

    //store the results
    this.setState({ board: newBoard, turn: newBoard['turn']});
    this.setState({playerPointVal: newBoard['player_points'][this.state.turn]})
    this.setState({deckSize: newBoard['deck'].length});

    //check if board is balanced then rebalance tree if fxn returned false

    let made_graph = create_graph(this.state.board['graph'])
    this.setState({ graph: made_graph});
    this.setState({loading: false})
  }

  //AI api call
  aiCall = async () => {
    let ai_url = url+"game_board/api/ai_pick/" + this.state.board['game_id'] + '/' + this.state.username + '/' + this.state.token

    this.setState({ loading: true});

    //make the API call
    let ai_response = await fetch(ai_url);
    let ai_board = await ai_response.json();

    //store the results
    this.setState({ board: ai_board, turn: ai_board['turn']});
    this.setState({playerPointVal: ai_board['player_points'][this.state.turn]})
    this.setState({deckSize: ai_board['deck'].length});

    // update the tree visual
    let made_graph = create_graph(this.state.board['graph'])
    this.setState({ graph: made_graph});
    this.setState({loading: false})
  }

  //check if game is over (ie: is golden node at the root of the tree/does API end_game == true?)
  checkGameStatus = async () => {

    //if the JSON has end_game = true, store that in the state
    if (this.state.board['end_game']){
      this.setState({game_over: true})
    }

    //introduced a timeout because of a bug that arose without it:
    //the state was updating before the API call returned,
    //and the game was ending 1 turn after it should have
    //setTimeout(this.checkBoard, 200)
  }

  //if the API can no longer find the game board in the db,
  //it was deleted because the game is over
  checkBoard = async () => {

    //API call to view state of the board
    let temp_url = url+"game_board/api/board/" + this.state.board['game_id']
    let resp = await fetch(temp_url);
    let temp_board = await resp.json();

    //if the game is no longer found, it is over
    if (temp_board["error"] == "Game Not Found!") {
      this.setState({game_over: true})
    }

  }

  // Create custom text content for the nodes: Node point and Node ID
  renderNodeText = (data) => {
    // text location
    let x = '-20';
    let y = '-45';

    // design class names
    let points_class_name = "text-4xl font-bold text-gray-900 dark:text-gray-200";
    let node_id_class_name =  "text-l font-semibold text-gray-800 dark:text-gray-200";

    // if points is single digit re-adjust its x coordinate position
    if (data.points < 10) {
      x = '-10';
    }

    // render the design
    return (
      <foreignObject x={x} y={y} width='200' height='250'>
        <div id="graph_node" className="flex items-center">
          <p className={points_class_name} id="node_points_text">{data.points}</p>
          <p className={node_id_class_name} id="node_id_text">   <br></br><br></br><br></br> {data.node_id}</p>
        </div>
      </foreignObject>
    );
  };

  repositionNodes = () =>{
    this.setState({
      layoutEngineType: 'SnapToGrid',
      read_only: false
    })
  }

  checkNodes = () => {
    this.setState({
      layoutEngineType: 'VerticalTree',
      read_only: true
    })

  }

  // Function to display all of the players in the gameboard
  playersDisplay = (player) => {

    // class for the main background in player displays
    let class_name_box = "space-y-5 flex items-center p-4 bg-white rounded-lg shadow-xs dark:bg-gray-800";
    let player_name = player;

    // class for player points display
    let class_name_points = "p-3 mr-4 text-4xl text-green-600 bg-white rounded-full dark:text-green-100 font-bold";

    // if points is less than 0: displays red alert
    if (this.state.board["player_points"][player] < 0) {
      class_name_points = "p-3 mr-4 text-4xl text-red-700 bg-white rounded-full font-bold animate-pulse-once";
    }


    // If it is the player who's turn it is to play: makes the box blue
    if (this.state.turn == player) {
      class_name_box = "space-y-5 flex items-center p-4 bg-blue-500 rounded-lg shadow-xs dark:bg-gray-800 shadow-2xl";
      player_name = "* " + player;
    }

    // Find the player with the highest points
    let winning_player = "";
    let winning_player_points = 0;
    this.state.board["player_ids"].map((curr_player, ii, arr) => {
        if (this.state.board["player_points"][curr_player] > winning_player_points) {
          winning_player_points = this.state.board["player_points"][curr_player];
          winning_player = curr_player;
        }
    });

    // Put a glowing alert on the winning player's display
    if (winning_player == player) {
      if (winning_player_points > 0) {
        class_name_points = "p-3 mr-4 text-4xl text-blue-800 bg-white rounded-full dark:text-green-100 font-bold animate-wiggle";
      }
    }

    // Get all of the cards as string to be displayed
    let cardsDisplay = "";
    this.state.board["cards"][player].map((card, ii, arr) => {
        if (arr.length - 1 === ii) {
            // last one
           cardsDisplay += card
        } else {
           cardsDisplay += card + " - "
        }
    });

    // Return HTML component cards with the information
    return (
          <div className={class_name_box}>
            <div className={class_name_points} name="player_points_display">
                {this.state.board["player_points"][player]}
            </div>
            <div>
              <p  className="text-l text-center font-bold text-gray-800 mb-2" name="player_name_display">
                {player_name}
              </p>
              <p className="text-m font-semibold text-gray-800 dark:text-gray-200" name="player_cards_display">
                {cardsDisplay}
              </p>
            </div>
          </div>
    )
  }

  saveGame = async () => {
    if (!this.state.initial_load && this.state.username != "-1" && this.state.token != "-1") {

      //store user input in FormData format
      let apiData = new FormData()
      apiData.append("user_id", this.state.username)
      apiData.append("game_id", this.state.gameID)
      apiData.append("token", this.state.token)

      //api call parameters
      let requestOptions = {
        method: 'POST',
        body: apiData,
        redirect: 'follow'
      };

      //make api call
      let fetch_url = url + "profile_page/api/save_board"
      let response = await fetch(fetch_url, requestOptions)

      //make sure api call was successful, display error message if not
      if (!response.ok) {
        Swal.fire({
          title: 'Failed to save game!',
          icon: 'error',
          text: "This game has already been saved."
        })
      }
    }
  }

  buildSaveButton = () => {

    if(!this.state.initial_load && this.state.username != "-1" && this.state.token != "-1") {
      return (
        <button data-delay-show='500' data-place="bottom" data-tip="Save the current game to profile" data-offset="{'top': -20}" data-text-color="yellow"
        className="transition duration-500 ease-in-out bg-green-500 hover:bg-green-600  transform hover:-translate-y-1 hover:scale-105   border-green-500  border-opacity-50 rounded-lg shadow-2xl flex-1 m-1 py-1 flex justify-center font-bold text-xl text-gray-800" 
        onClick={() =>this.saveGame()}>Save Game</button>


      )
    }
  }

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

    // Deck size visual
    let deck_size_visual = "text-xl font-semibold text-gray-800 dark:text-gray-200";
    if (this.state.deckSize <= 5) {
      deck_size_visual = "text-xl font-semibold text-red-700 animate-pulse";
    }


    //if loading is completed, statically store cards
    if (!this.state.loading) {
      // here staticly getting the cards so change, plus it would have to be updateding as we play
      card_1 = this.state.board['cards'][this.state.board['turn']][0]
      card_2 = this.state.board['cards'][this.state.board['turn']][1]
      card_3 = this.state.board['cards'][this.state.board['turn']][2]
    }

    if (!this.state.loading) {  // if changes are not being made
        this.checkGameStatus()  // update win condition
        if (!this.state.game_over) {  // if game is still ongoing
            if (this.state.turn.replace(/\s+/g, "").toLowerCase().startsWith('bot')) {  // if its the bots turn
                this.aiCall()
            }
        }
        if(!this.checkRebalance() && !this.state.turn.replace(/\s+/g, "").toLowerCase().startsWith('bot')){
            this.rebalance()
        }
    }

    //html returned to display page. When each card is played, the appropriate function is called, which in turn makes an API call
    return (

      <div>
        <Particles
              id="particles2"
              params={{
                particles: {
                  color:"#000000",
                  line_linked: {
                    color:"#000000",
                    distance:50,
                  },
                  number: {
                    value: 38,
                    density: {
                      enable: true,
                      value_area: 500,
                    }
                  },
                  move:{
                    direction:"bottom",
                    random:true,
                    speed:1,
                    out_mode:"out",
                  }
                },
              }}
        />

        <div className="flex mb-4 flex justify-center space-x-4">
            { !this.state.initial_load && this.state.playersArray.map((player) => this.playersDisplay(player)) }
        </div>


        <div style={{height: "10rem"}}>

          {this.state.game_over ? <WinModal winner={this.state.turn} win_board={this.state.board}/> : <div> </div>}

          <div className="flex items-center bg-opacity-0 h-11">

            <button className="transition duration-500 ease-in-out bg-blue-500 hover:bg-red-500 transform hover:-translate-y-1 hover:scale-105 bg-blue-300 border-blue-350 border-opacity-50 rounded-lg shadow-2xl flex-1 m-1 py-1 flex justify-center font-bold text-xl text-gray-800" onClick={() => this.playCard(card_1)}>{card_1}</button>
            <button className="transition duration-500 ease-in-out bg-blue-500 hover:bg-red-500 transform hover:-translate-y-1 hover:scale-105 bg-blue-300 border-blue-350 border-opacity-50 rounded-lg shadow-2xl flex-1 m-1 py-1 flex justify-center font-bold text-xl text-gray-800" onClick={() => this.playCard(card_2)}>{card_2}</button>
            <button className="transition duration-500 ease-in-out bg-blue-500 hover:bg-red-500 transform hover:-translate-y-1 hover:scale-105 bg-blue-300 border-blue-350 border-opacity-50 rounded-lg shadow-2xl flex-1 m-1 py-1 flex justify-center font-bold text-xl text-gray-800" onClick={() => this.playCard(card_3)}>{card_3}</button>

            <div
                className="flex justify-center">
              <div className="flex items-center p-4 bg-white rounded-lg shadow-xs dark:bg-gray-800">
                <div
                    className="p-3 mr-4 text-orange-500 bg-orange-100 rounded-full dark:text-orange-100 dark:bg-orange-500">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path
                        d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"></path>
                  </svg>
                </div>
                <div>
                  <p className={deck_size_visual} id="deck_size_display">
                    Remaining Turns: {this.state.deckSize}
                  </p>
                </div>
              </div>
            </div>

              <button data-delay-show='500' data-place="bottom" data-tip="Shift click to make edges, delete a selected node with the keyboard's delete key" data-offset="{'top': -20}" data-text-color="yellow"
                  className="transition duration-500 ease-in-out bg-orange-500 hover:bg-orange-600  transform hover:-translate-y-1 hover:scale-105 border-orange-500 border-opacity-50 rounded-lg shadow-2xl flex-1 m-1 py-1 flex justify-center font-bold text-xl text-gray-800" onClick={() =>this.repositionNodes()}>Reposition Nodes</button>

              <button data-delay-show='500' data-place="bottom" data-tip="End's turn and determines rebalance correctness" data-offset="{'top': -20}" data-text-color="yellow"
                  className="transition duration-500 ease-in-out bg-orange-500 hover:bg-orange-600  transform hover:-translate-y-1 hover:scale-105   border-orange-500  border-opacity-50 rounded-lg shadow-2xl flex-1 m-1 py-1 flex justify-center font-bold text-xl text-gray-800" onClick={() =>this.checkNodes()}>Check Nodes</button>

              {this.buildSaveButton()}

        </div>

        <ReactTooltip />
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
          readOnly={this.state.read_only}
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
//const rootElement = document.getElementById("root");
//ReactDOM.render(<GameBoard />, rootElement);
