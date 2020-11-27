import React, { Component } from 'react'
import "./styles.css";
import Particles from 'react-particles-js';
import GameInfo from './Modal/GameInfo.js'
import { RankingTable } from './RankingTable'

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

            <div className="flex items-center justify-center h-screen">
                <GameInfo className="flex items-center justify-center h-screen"
                    level = {this.state.difficulty}
                    playerList={this.state.players}
                    gameDS={this.state.data_structure}
                />
            </div>

            <div className="space-y-30 flex justify-center">
                <div className='Rankings'>
                  <RankingTable />
                </div>
            </div>

    </div>

    )
}
}
export default Home