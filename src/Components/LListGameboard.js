import React, { Component } from "react";
import './LListGameboard.css';
import Stats from './LListStats';

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
    //previous team added cookies... look into that

    //API call
    let response = fetch(url + "game_board/llist_api")



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