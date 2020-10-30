import React, { Component } from 'react'
import "./styles.css";
import Particles from 'react-particles-js';
import { Button} from '@material-ui/core';
import GameInfo from './Modal/GameInfo.js'
//this function is called from App.js to start the interface of the game
//calls the GameInfo modal to get the new game's information
class Home extends Component{
  //constructor to set the intial state value's
  constructor(props) {
    super(props);
    this.state = {
      difficulty:null,
      players:null,
      data_structure:null
    };
  }
  //display the background particle
  //and the modal as a button and pass the state values in there
  render(){
    return(
    <div>

        <Particles
            id="particles"
            params={{
              particles: {
                color:"#000000",
                line_linked: {
                  color:"#000000",
                },
                number: {
                  value: 80,
                  density: {
                    enable: true,
                    value_area: 800,
                  }
                },
              },
            }}
          />

        <h1 >Enter Game Info</h1>
        <Button>
        <GameInfo
        level = {this.state.difficulty}
        playerList={this.state.players}
        gameDS={this.state.data_structure}
        />
    </Button>
    
    </div>
    )
}
}
export default Home