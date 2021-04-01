import React, { Component } from "react";
import './Stats.css';

// shows the in  game stats in the upper right corner of game page
// hardcoded values for now
class Stats extends Component {

  render() {
    return (
      <div className="stats-row">
        <div className="stats">
          <p>TIME</p>
          <p>FOOD</p>
          <p>ANTS</p>
          <p>CHAMBERS</p>
        </div>
        <div className="stats-values">
          <p>0</p>
          <p>0</p>
          <p>0</p>
          <p>0</p>
        </div>
      </div>

    )
  }
}
export default Stats