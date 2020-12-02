import React, { Component } from "react";
import Particles from 'react-particles-js';

class Tutorial extends Component{

    //constructor to set the intial state value's
    constructor(props) {
      super(props);
      this.state = {
        difficulty:null,
        players:null,
        data_structure:null
      };
    }

    //display the background particle
    //and the modal as a button and pass the state values in there
    render(){

      return(

      <div>

          <Particles
              id="particles"
              params={{
                particles: {
                  color:"#000000",
                  line_linked: {
                    color:"#000000",
                  },
                  number: {
                    value: 80,
                    density: {
                      enable: true,
                      value_area: 800,
                    }
                  },
                },
              }}
            />




      </div>

      )
  }
  }
  export default Tutorial