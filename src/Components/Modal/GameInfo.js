import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {Button, Grid, TextField} from '@material-ui/core';
import { render } from '@testing-library/react';
import Cookies from 'universal-cookie';


class GameInfo extends React.Component {
    constructor(props) {
        super(props);
        this.customNodeRef = React.createRef();
        //let hyparlink = props.hyparlink || new Hyparlink();
        this.state = {level:null, playerList:null, gameDS:'AVL'};
        this.handleInput = this.handleInput.bind(this);
        this.submitDSG = this.handleInput.bind(this)
    }


    handleInput = (e) => {
        this.setState({ [e.target.name]: e.target.value });
        console.log(this.state)

        const cookies = new Cookies();
        cookies.set('level', this.state.level, { path: '/' });
        cookies.set('playerList', this.state.playerList, { path: '/' });
        cookies.set('gameDS', this.state.gameDS, { path: '/' });
    };



render(){

    return(
        <form>
        <Grid container spacing={1} style={{ marginBottom: '5em' }}>
            <Grid item sm={6} md={6} lg={6}>

                <select value={this.state.level} onInput={this.handleInput} name='level' label='Difficulty Level' style={{ marginBottom: '1em' }}  >
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
                 </select>

                <select value={this.state.gameDS} onInput={this.handleInput} name='gameDS' label='DSgame' style={{ marginBottom: '1em' }}  >
                    <option value="AVL">AVL</option>
                    <option value="Stack">Stack</option>
                 </select>

                <TextField
                    required
                    fullWidth
                    name='playerList'
                    label='players'
                    value={this.state.playerList}
                    onChange={this.handleInput}
                    style={{ marginBottom: '1em' }}
                />

            </Grid>
            </Grid>
             </form>

    );
}
}
export default GameInfo;
