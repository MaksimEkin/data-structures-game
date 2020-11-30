//JS file for modal that displays when game ends
import React, { Component } from 'react';
import Swal from "sweetalert2"


//Modal that displays when game is won
class WinModal extends Component {

    constructor(props) {
        super(props);

        //props sent over are winner and the state of the game board at time of win
        this.state = {
            modal: this.props.modal,
            turn: this.props.winner
        }
    }
    hideModal(){
        this.setState({modal:false})

    }

    render() {

        //Display win message
        Swal.fire({
            //display winner score
            title: "UNBALANCED BOARD, PLAYER: " + this.state.turn,
            
            //display other players' scores
            text: "TIME TO REBALANCE",
            confirmButtonText: "Start",
        }).then((result) => {
            if (result.isConfirmed) {
                this.props.parentCallback(false);
                console.log('in rebalanceModal, parentCallback is ',this.props.parentCallback)
            }
        })
        return (<div> </div>)
    }
}

export default WinModal;