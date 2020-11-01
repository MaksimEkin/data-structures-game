//JS file for modal that displays when game ends
import React, { Component } from 'react';
import Swal from "sweetalert2"
import Party_Face from "../Party Face.svg"

//Modal that displays when game is won
class WinModal extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        Swal.fire({
            title: "Congrats! You are the Data Structures Wizard!",
            imageUrl: Party_Face
        });
        return (<div> </div>)
    }
}

export default WinModal;