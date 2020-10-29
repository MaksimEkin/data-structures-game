//JS file for modal that displays when game ends
import React, { Component } from 'react';
import {Button, Dialog} from "@material-ui/core";

class WinModal extends Component {

    constructor(props) {
        super(props);
    }

    render() {

    return (
        <div>
            <Button onClick={() => { alert('closed')}} > Click me </Button>
            <h1> Testing Modal </h1>
        </div>
        );
}
}

export default WinModal;