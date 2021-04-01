import React, { Component } from "react";
import './LListGameboard.css';
import Stats from './LListStats';

//this allows us to test separately locally and on Heroku by changing just one line
const local = "http://127.0.0.1:8000/";
const reactLocal = "http://localhost:3000/"
const remote = "https://data-structures-game.herokuapp.com/";

const url = local;


//export default function App() {
class App extends Component {

  // constructor with default values
  constructor(props) {
    super(props);
    this.state = {
      // in-game stats
      food: 0,
      time: 0,
      numChambers: 0,
      numAnts: 2,

    };
  }

  render() {
    return (
      <div className="gamepage">
        <div className="title">
          <p>Linked List</p>
        </div>

        <div className="stats-container">
          <Stats />
        </div>


      </div>
    );
  }
}

export default