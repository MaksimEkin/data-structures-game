import React, { Component } from 'react'
import Header from './Header'
import "./styles.css";
import Particles from 'react-particles-js';
import { Button, Grid, Typography, Card, CardHeader, CardActions, CardActionArea, CardContent, Chip } from '@material-ui/core';
import GameInfo from './Modal/GameInfo.js'
//function Home(){
class Home extends Component{
  constructor(props) {
    super(props);
    this.state = {
      difficulty:null,
      players:null,
      data_structure:null
    };
  }



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

        <h1 className="font-bold text-2xl"> Home</h1>
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