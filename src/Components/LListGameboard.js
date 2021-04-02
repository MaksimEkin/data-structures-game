import React, { Component } from "react";
import './LListGameboard.css';
import Stats from './LListStats';
import Cookies from 'universal-cookie';

//this allows us to test separately locally and on Heroku by changing just one line
const local = "http://127.0.0.1:8000/";
const reactLocal = "http://localhost:3000/"
const remote = "https://data-structures-game.herokuapp.com/";

const url = local;


//export default function App() {
class LListGameboard extends Component {
  // constructor with default values
  constructor(props) {
    super(props);
    this.state = {
      // game settings
      difficulty:null,
      gameMode:null,
      players:null,
      board: null,
      gameID: null,
      token: "-1",
      username: "-1",
      ds: null,

      // in-game stats
      food: 1,
      time: 0,
      numChambers: 3,
      numAnts: 2,

      loading: true,

    };
  }

  //component rendered at least once
  // fetch the data here
  async componentDidMount() {

    const cookies = new Cookies();

    // get variables used in url
    let difficulty = cookies.get('level');
    let players = cookies.get('playerList');
    let ds = cookies.get('gameDS');

    if (cookies.get('username') != null && cookies.get('token') != null) {
      if (cookies.get('username') != "" && cookies.get('token') != "") {
        this.setState({ username: cookies.get('username'), token: cookies.get('token') })
        players = players + "," + cookies.get('username');
      }
    }

    // add cookie variables to url
    let createGameURL = url + "game_board/llist_api/start_game/" + difficulty + "/" + players + "/" + ds
    let getGameURL = url + "game_board/llist_api/board/";

    /*
    //API call to start game
    let response = fetch(createGameURL);
    let game_id = await response.json();

    // save the get request response
    this.setState({ gameID: game_id['game_id']});
    cookies.set('game_id', game_id['game_id'], { path: '/'});

    //get request to api and include the dynamic game_id
    response = await fetch(getGameURL + game_id['game_id']);
    let game_board = await response.json();

    //set the state value from json response
    this.setState({ board: game_board });
    */


  }

  render() {
    return (
      <div className="gamepage">
        <div className="title">
          <p>Linked List</p>
        </div>

        <div className="stats-container">
          <Stats time={this.state.time} food={this.state.food} ants={this.state.numAnts} chambers={this.state.numChambers}/>
        </div>


      </div>
    );
  }
}

export default LListGameboard