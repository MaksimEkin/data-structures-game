import React, { useState } from 'react'; 
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {Button, Grid, TextField} from '@material-ui/core';
import { render } from '@testing-library/react';
class GameInfo extends React.Component {
    constructor(props) {
        super(props);
        this.customNodeRef = React.createRef();
        //let hyparlink = props.hyparlink || new Hyparlink();
        this.state = {difficulty:null, players:null, data_structure:null, game_id:null};
        this.handleInput = this.handleInput.bind(this); //bind to the input when target value changes
    }   
    handleInput = ({ target }) => {
        this.setState({ [target.name]: target.value });
        console.log(this.state)
    };
   getURLfxn =()=>
    {
        let levelU= this.state.difficulty
        let playerListU = this.state.players
        let gameDSU = this.state.data_structure
        
        let start_game_url="/game_board/api/start_game/"+ {levelU}+"/"+{playerListU}+"/"+{gameDSU}
        console.log(start_game_url)
        fetch({start_game_url})
        .then(response => response.json())
        .then(data => this.setState({ game_id: data.total }));
        console.log(this.state.game_id)

        
    }
   
render(){
    this.getURLfxn()
    return(
        <Grid container spacing={1} style={{ marginBottom: '5em' }}>
            <Grid item sm={6} md={6} lg={6}>
                <TextField 
                    required 
                    fullWidth
                    name='level'
                    label='Difficulty Level' 
                    value={this.state.difficulty} 
                    onChange={this.handleInput} 
                    style={{ marginBottom: '1em' }} 
                />
                <TextField 
                    required
                    fullWidth
                    name='playerList' 
                    label='players'
                    value={this.state.players} 
                    onChange={this.handleInput} 
                    style={{ marginBottom: '1em' }} 
                />
                <TextField 
                    fullWidth 
                    multiline 
                    name='gameDS' 
                    label='DSgame'
                    value={this.state.data_structure} 
                    onChange={this.handleInput} 
                    style={{ marginBottom: '1em' }} 
                />            
            </Grid>
            

            </Grid>
                
    );
}
}
export default GameInfo;
