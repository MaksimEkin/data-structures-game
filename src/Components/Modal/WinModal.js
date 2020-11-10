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

        //string to store other players' scores
        let playerScores = ""

        //loop through all players in board
        for (i = 0; i < this.state.board["num_players"]; i++){

            //don't include winner in the list of other players (their score displayed separately)
            if (!(this.state.board["player_ids"][i] == this.state.winner)){

                //get id of player (not a winner)
                let curPlayer =  this.state.board["player_ids"][i]
                playerScores += curPlayer

                //and their score
                playerScores += " with " + this.state.board.player_points[curPlayer] + " points!,"
            }
        }

        //slice off last comma
        playerScores = playerScores.substring(0, playerScores.length - 1)

        //Display win message
        Swal.fire({
            //display winner score
            title: "Congrats " + this.state.winner + "! You are a Data Structures Wizard, with "
                + this.state.board["player_points"][this.state.winner] + " points!",

            //display other players' scores
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