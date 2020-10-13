import React from 'react';
import logo from './logo.svg';
import Home from './Components/Home'
import Header from './Components/Header';

function App() {
  return (
    <div className="App">
      <header className="App-header">
  {/* <img src={logo} className="App-logo" alt="logo" */}
            <Header />
      </header>
    </div>
  );
}

export default App;
