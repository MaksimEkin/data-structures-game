import React, { useState } from 'react'; 
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {Button, Grid, TextField} from '@material-ui/core';
import { render } from '@testing-library/react';
class GameInfo extends React.Component {
    constructor(props) {
        super(props);
        //let hyparlink = props.hyparlink || new Hyparlink();
        this.state = {level:null, playerList:null, gameDS:null};
    }

render(){
    return(
        <Grid container spacing={1} style={{ marginBottom: '5em' }}>
            <Grid item sm={6} md={6} lg={6}>
                <TextField 
                    required 
                    fullWidth
                    id='level-input'
                    label='Difficulty Level' 
                    value={this.state.level} 
                    onChange={e => this.handleInput('Hard, Medium, Easy', e.target.value)} 
                    style={{ marginBottom: '1em' }} 
                />
                <TextField 
                    required
                    fullWidth
                    id='playerList-input' 
                    label='players'
                    value={this.state.playerList} 
                    onChange={e => this.handleInput('Players (comma separated)', e.target.value)} 
                    style={{ marginBottom: '1em' }} 
                />
                <TextField 
                    fullWidth 
                    multiline 
                    id='DS-input' 
                    label='DSgame'
                    value={this.state.gameDS} 
                    onChange={e => this.handleInput('AVL', e.target.value)} 
                    style={{ marginBottom: '1em' }} 
                />            
            </Grid>
            <Button>


                
            </Button>
         </Grid>
                
    );
}
}
export default GameInfo;
