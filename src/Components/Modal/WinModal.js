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
        let playerScores = ""
        for (i = 0; i < this.state.board["num_players"]; i++){
            if (!(this.state.board["player_ids"][i] == this.state.winner)){
                let curPlayer =  this.state.board["player_ids"][i]
                playerScores += curPlayer
                playerScores += " with " + this.state.board.player_points[curPlayer] + " points, \n"
            }
        }
        console.log("PlayerScores: ", playerScores)
        /*console.log("In Win Modal, printing board", this.state.board)
        var i
        let players = []
        for (i = 0; i < this.state.board["num_players"]; i++) {
            console.log(this.state.board["player_ids"][i])
            console.log("winner", this.state.winner)
            if (!(this.state.board["player_ids"][i] == this.state.winner)) {
                console.log("In if")
                players.push(this.state.board["player_ids"][i])
            }
        }

        var j
        let playerList = ""
        for (j = 0; j < players.length; j++){
            playerList += players[j] + "\n"
        }

        console.log("PlayerList, ", playerList)

        console.log("Player points", this.state.board.player_points[players[0]]);
/*
        let testing = ""
        for (i = 0; i < this.state.board["num_players"]; i++){
            testing += players[i]
            testing += this.state.board["player_points"][[players][i]]
        }

        console.log("Testing: ", testing) */


        //Display win message
        Swal.fire({
            title: "Congrats " + this.state.winner + "! You are a Data Structures Wizard, with "
                + this.state.board["player_points"][this.state.winner] + " points!",
            text: "Other all-stars: " + playerScores,
            imageUrl: Party_Face,
            confirmButtonText: "Return to Home Page"
        }).then((result) => {

            //if player clicks "Return to Home Page" button, redirect there
            if (result.isConfirmed) {
                window.location.href = "/"
            }
        })
        return (<div> </div>)
    }
}

export default WinModal;