//JS file for modal that displays when game ends
import React, { Component } from 'react';
import Swal from "sweetalert2"


//Modal that displays when game is won
class WinModal extends Component {

    constructor(props) {
        super(props);

        //props sent over are winner and the state of the game board at time of win
        this.state = {
            
            turn: this.props.winner
        }
    }

    render() {

        //Display win message
        Swal.fire({
            //display winner score
            title: "UNBALANCED BOARD, PLAYER: " + this.state.winner,

            //display other players' scores
            text: "TIMEE TO REEBALANCEE",
            confirmButtonText: "Return to Home Page"
        
        })
        return (<div> </div>)
    }
}

export default WinModal;