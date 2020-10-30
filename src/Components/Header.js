import React from 'react'
import GameBoard from './GameBoard'
import Home from './Home'
import {Route, Link, Switch} from "react-router-dom";
import { BrowserRouter as Router } from 'react-router-dom'
import NavMenu from './NavMenu';
//header component called in every page and displays its child component to display the menu
function Header(){
    return(
<header className="border-b p-3 flex justify-between items-center">
        Data Structures Game

    <NavMenu />
        </header>

        
    )   
}
export default Header