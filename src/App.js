//import React from 'react';
import React from "react";
import GameBoard from './Components/GameBoard'
import Home from './Components/Home'
import Profile from './Components/Profile'
import Login from './Components/Login'
import Header from './Components/Header';
import {Route, Switch} from "react-router-dom";
import { BrowserRouter as Router } from 'react-router-dom'
//react router used to make this web app multiple pages instead of single page application
function App(){
  return (
    <div>      
    <Router>
    <Header />
     
      <Switch>
        <Route exact path="/">
          <Home/>
        </Route>
        <Route exact path="/game_board">
          <GameBoard/>
        </Route>
        <Route exact path="/login">
          <Login/>
        </Route>
      </Switch>
    </Router>      
    </div>      
  );
}

export default App;
