//JS file for modal that displays when game ends
import React, { Component } from 'react';
import Swal from "sweetalert2"
import Party_Face from "../Party Face.svg"

//Modal that displays when game is won
class WinModal extends Component {

    constructor(props) {
        super(props);

        //props sent over are winner and the state of the game board at time of win
        this.state = {
            board: this.props.win_board,
            winner: this.props.winner
        }
    }

    render() {
        var i
        let players = []
        for (i = 0; i < this.state.board["num_players"]; i++) {
            console.log(this.state.board["player_ids"][i])
            players.push(this.state.board["player_ids"][i])
        }

        let testing = ""
        for (i = 0; i < this.state.board["num_players"]; i++){
            testing += this.state.board["player_ids"][i]
            testing += this.state.board["player_points"][[players][i]]
        }

        console.log("Testing: ", testing)


        console.log("Winner: ", this.state.winner)
        Swal.fire({
            title: "Congrats! You are the Data Structures Wizard!",
            text: "Winner is: " + this.state.winner + " with " + this.state.board["player_points"][this.state.winner] + " points!",
            imageUrl: Party_Face
        });
        return (<div> </div>)
    }
}

export default WinModal;