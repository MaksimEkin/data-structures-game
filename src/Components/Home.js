import React, { Component } from 'react'
import "./styles.css";
import Cookies from 'universal-cookie';
import Particles from 'react-particles-js';
import GameInfo from './Modal/GameInfo.js'
import { RankingTable } from './RankingTable'

//this allows us to test separately locally and on Heroku by changing just one line
const local = "http://127.0.0.1:8000/";
const reactLocal = "http://localhost:3000/"
const remote = "https://data-structures-game.herokuapp.com/";

//can also be const url = local; or const url = reactLocal;
const url = remote;

//this function is called from App.js to start the interface of the game
//calls the GameInfo modal to get the new game's information
class Home extends Component{

  //constructor to set the intial state value's
  constructor(props) {
    super(props);
    this.state = {
      difficulty:null,
      players:null,
      data_structure:null,
      data:[{"id":0,"user_name":"test","total_score":0}]
    };
  }

  async componentDidMount() {
      //remove current gameboard (if applicable)
      const cookies = new Cookies();
      
      if ((cookies.get('loaded_game')) && (cookies.get('loaded_game') != '')) {
        cookies.remove('loaded_game', { path: '/' })
        cookies.set('loaded_game', '', { path: '/' })
      }

      //assemble api call 
      let rankingsURL = url + "api/rankings/" + 20;
      let response = await fetch(rankingsURL);
      let rank_head = await response.json();
      this.setState({ data: rank_head['top_ranking_players'] })


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
                  <RankingTable
                    data = {this.state.data} 
                  />
                </div>
            </div>

    </div>

    )
}
}
export default Home