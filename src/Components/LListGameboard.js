import React, { Component } from "react";
import './LListGameboard.css';
import Stats from './LListStats';
import Cookies from 'universal-cookie';
import Queen from './antqueen.png';
import Ant from './ant.png';

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
      food: 3,
      time: 0,
      numChambers: 0,
      numAnts: 1,

      loading: true,
      spawningAnt: false,

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

  // api call to spawn an ant
  spawnAnt = () =>{
    
    
  };

  // startHover and endHover are used when mouse is hovering over queen ant 
  startHover = () =>{
    this.setState({hovering: true})
  }
  endHover = () => {
    this.setState({hovering: false})
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

        {this.state.hovering? 
        <rect style={{width:"160px", height:"130px", background:"white", opacity:".5", position:"absolute", top:"44%", left:"27%", border:"10px solid rgba(255, 255, 255, .5)", borderRadius:"5px"}}/>
        : null}
        {this.state.hovering? 
        <p style={{fontSize:"12px", position:"absolute", top:"44%", left:"27.5%"}}>Click to spawn worker ant</p>
        : null}
        <span>
          <button><img src={Queen} width ="130" style={{position:'absolute', top: '45.5%', left:'28%', padding:"5px 5px"}} 
          onMouseOver ={this.startHover} onMouseOut = {this.endHover}
          onClick={this.spawnAnts}/></button>
        </span>
        

      </div>
    );
  }
}

export default LListGameboard