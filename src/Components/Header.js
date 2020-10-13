import React from 'react'
import Navigation from './Navigation'
import GameBoard from './GameBoard'
import Home from './Home'
import {Route, Link, Switch} from "react-router-dom";
import { BrowserRouter as Router } from 'react-router-dom'
function Header(){
    return(
        <header className="border-dotted border-4 border-gray-600 font-bold p-5 flex justify-center ">
        Data Structures Game
          
    {/* <Navigation /> */}
        </header>
    )   
}
export default Header