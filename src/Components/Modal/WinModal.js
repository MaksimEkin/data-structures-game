//JS file for modal that displays when game ends
import React, { Component } from 'react';
//import {Button, Modal} from "react-bootstrap";
import Swal from "sweetalert2"
import Party_Face from "../Party Face.svg"

class WinModal extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        Swal.fire({
            title: "Congrats! You are the Data Structures Wizard",
            imageUrl: Party_Face
        });
        return (<h1> For return </h1>)


    /*return (
        <div>
            <Button> Open Modal </Button>
            <Modal show={true} >
            <Modal.Header> GAME OVER </Modal.Header>
            <Modal.Body> This is the body </Modal.Body>

            <Modal.Footer>
                This is the footer
            </Modal.Footer>

            </Modal>
        </div>
        );*/
}
}

export default WinModal;