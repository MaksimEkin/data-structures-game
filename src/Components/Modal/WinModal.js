//JS file for modal that displays when game ends
import React, { Component } from 'react';
import {Button, Modal} from "react-bootstrap";

class WinModal extends Component {

    constructor(props) {
        super(props);
    }

    render() {

    return (
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
        );
}
}

export default WinModal;