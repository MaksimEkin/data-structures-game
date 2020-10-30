//import React from 'react';
import React from "react";
import GameBoard from './Components/GameBoard'
import Home from './Components/Home'
import Header from './Components/Header';
import {Route, Link, Switch} from "react-router-dom";
import { BrowserRouter as Router } from 'react-router-dom'

 
function App(){
  return (
    <div>      
    <Router>
    <Header />
      <ul>
        <li>
          <Link className="text-blue-500 py-3 border-t bordre-b block" to="/" >
            Home
          </Link>
        </li>
        <li>
          <Link className="text-blue-500 py-3 border-t bordre-b block" to="/game_board" name="start_game">
            Start Game</Link>
        </li>
      </ul>
      <Switch>
        <Route exact path="/">
          <Home/>
        </Route>
        <Route exact path="/game_board">
          <GameBoard/>
        </Route>
      </Switch>
    </Router>      
    </div>      
  );
}

export default App;
