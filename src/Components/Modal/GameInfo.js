import React from 'react';
import {Button, TextField} from '@material-ui/core';
import Cookies from 'universal-cookie';
import {Link} from "react-router-dom";

//set the construct by sharing/setting the constructor states between
// Home and GameInfo & bind the state value's to the input change that happens
class GameInfo extends React.Component {
    constructor(props) {
        super(props);
        this.customNodeRef = React.createRef();
        //hard coded defaults
        this.state = {level:'Easy', playerList:'player1,bot1', gameDS:'AVL'};
        this.handleInput = this.handleInput.bind(this);
        this.submitDSG = this.handleInput.bind(this)
        //defined cookie in constructor with initial values 
        const cookies = new Cookies();
        cookies.set('level', this.state.level, { path: '/' });
        cookies.set('playerList', this.state.playerList, { path: '/' });
        cookies.set('gameDS', this.state.gameDS, { path: '/' });
        
    }

    //this handls the change in input and is later binded to state values
    //cookies then are set to the changed values
        handleInput = async (e) => {
        await this.setState({ [e.target.name]: e.target.value });
        console.log(this.state)

        
        this.cookies.set('level', this.state.level, { path: '/' });
        this.cookies.set('playerList', this.state.playerList, { path: '/' });
        this.cookies.set('gameDS', this.state.gameDS, { path: '/' });
    };

render(){

    return(
        //grid stores the different options that are set in the modal form
        // each value input changes handleInput and is rebinded to the state value
        //that is changed and resets the cookies

        <div className="w-full md:max-w-md mt-6">
            <span>
            <div className="card bg-gray-200 shadow-2xl rounded-2xl px-4 py-4 mb-4 ">

            <div className="space-y-10 flex justify-center">
              <h1 className="space-y-20 text-3xl text-center font-semibold text-gray-800 mb-2">Data Structures Game</h1>
          </div>

        <form onSubmit={this.handleSubmit}  >

        <div className="form-group" className="space-y-2">
        <label className="text-xl text-center font-semibold text-gray-800 mb-2"
               htmlFor='game'>Data Structure     </label>
                <select type='text' id="game" value={this.state.gameDS} onInput={this.handleInput} name='gameDS'
                        label='DSgame' style={{marginBottom: '1em'}}>
                    
                    <option value="AVL">AVL</option>

                 </select>
        </div>

        <div class="form-group" className="space-y-2">
        <label  className="text-xl text-center font-semibold text-gray-800 mb-2" for='difficulty-level'>Difficulty     </label>
                <select type='text' id='difficulty-level' value={this.state.level} name='level' onChange={this.handleInput} label='Difficulty Level' style={{ marginBottom: '1em' }}  >
                    
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
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

            <div className="space-y-10"><br></br></div>

                <ul>
                <li>
                    <Link className="shadow transition duration-500 ease-in-out bg-blue-500 hover:bg-red-500 transform hover:-translate-y-1 hover:scale-105 bg-blue-300 border-blue-350 border-opacity-50 rounded-lg shadow-xl p-5 rounded text-xl font-bold" to="/game_board" name="start_game">
                        Start Game
                    </Link>
                </li>
                </ul>

             <div className="space-y-10"><br></br></div>

                </form>

        </div></span></div>

    );
}
}
export default GameInfo;