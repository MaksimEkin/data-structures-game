import React, { useState } from 'react';
import {Button, Grid, TextField} from '@material-ui/core';
import Cookies from 'universal-cookie';

//set the construct by sharing/setting the constructor states between
// Home and GameInfo & bind the state value's to the input change that happens
class GameInfo extends React.Component {
    constructor(props) {
        super(props);
        this.customNodeRef = React.createRef();
        //hard coded defaults 
        this.state = {level:'Easy', playerList:'player1,player2', gameDS:'AVL'};
        this.handleInput = this.handleInput.bind(this);
        this.submitDSG = this.handleInput.bind(this)
    }

    //this handls the change in input and is later binded to state values
    //cookies then are set to the changed values
        handleInput = async (e) => {
        await this.setState({ [e.target.name]: e.target.value });
        console.log(this.state)

        const cookies = new Cookies();
        cookies.set('level', this.state.level, { path: '/' });
        cookies.set('playerList', this.state.playerList, { path: '/' });
        cookies.set('gameDS', this.state.gameDS, { path: '/' });
    };



render(){

    return(
        //grid stores the different options that are set in the modal form
        // each value input changes handleInput and is rebinded to the state value
        //that is changed and resets the cookies
        <span class="border border-secondary">
        <form>
<<<<<<< HEAD
        <div class="form-group">
        <label for='difficulty-level'>Difficulty Level</label>
                <select type='text' id='difficulty-level' value={this.state.level} name='level' onChange={this.handleInput} label='Difficulty Level' style={{ marginBottom: '1em' }}  >
=======
        <Grid container spacing={1} style={{ marginBottom: '5em' }}>
            <Grid item sm={6} md={6} lg={6}>

                <select id = 'level_select' value={this.state.level} onInput={this.handleInput} name='level' label='Difficulty Level' style={{ marginBottom: '1em' }}  >
>>>>>>> Added id's to select menus (to help wth testing)
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
                 </select>
<<<<<<< HEAD
        </div>
        <div class="form-group">
        <label for='game'>Tree Type  </label>
                <select type='text' id="game" value={this.state.gameDS} onInput={this.handleInput} name='gameDS' label='DSgame' style={{ marginBottom: '1em' }}  >
=======

                <select id = 'structure-select' value={this.state.gameDS} onInput={this.handleInput} name='gameDS' label='DSgame' style={{ marginBottom: '1em' }}  >
>>>>>>> Added id's to select menus (to help wth testing)
                    <option value="AVL">AVL</option>
                    
                 </select>
        </div>
                <TextField
                    required
                    fullWidth
                    name='playerList'
                    label='players'
                    value={this.state.playerList}
                    onChange={this.handleInput}
                    style={{ marginBottom: '1em' }}
                />

                <button type="submit">Sign In</button>
             </form>
             </span>

    );
}
}
export default GameInfo;
