import React from "react";
import GameBoard from './Components/GameBoard'
import Home from './Components/Home'
import Profile from './Components/Profile'
import Header from './Components/Header';
import {Route, Switch} from "react-router-dom";
import { BrowserRouter as Router } from 'react-router-dom'

//react router used to make this web app multiple pages instead of single page application
export default function App() {
  return (
    <Router>
      <div>
        <Header />
        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/game_board">
            <GameBoard />
          </Route>
          <Route path="/profile_page">
            <Profile />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}