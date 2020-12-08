import React, { Component } from "react";
import Particles from 'react-particles-js';

class Tutorial extends Component{

    //constructor to set the intial state value's
    constructor(props) {
      super(props);
    }

    render(){
  
      return(
          <div>
             { /* Display Game Tutorial videos */ }
             <div class="text-center">
              <h1 className="text-center font-bold text-2xl"> Game Tutorials </h1>
              <div className="items-center inline-flex">
                <iframe class="p-4 ml-8" width="450" height="300" src="https://www.youtube.com/embed/BvG2PfCWTE0" frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen></iframe>
                <iframe class="p-4" width="450" height="300" src="https://www.youtube.com/embed/accUNOfEgtk" frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen></iframe>
                <iframe class="p-4" width="450" height="300" src="https://www.youtube.com/embed/kr5YIyw39zI" frameBorder="0"
                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                          allowFullScreen></iframe>
              </div>
             </div>

              {/* space dividers */}
              <br />
              <br />

              <div>

                {/* Display particles effect */}
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

              {/* AVL Tree Resources */}
              <h1 className="text-center font-bold text-2xl">Resources on AVL Trees</h1>
              <br />
              <h2 className="text-center text-gray-600 underline font-bold text-xl"> Articles </h2>
          <div class="text-center font-semibold text-blue-400 underline">
                <a href="https://www.geeksforgeeks.org/avl-tree-set-1-insertion"> Geeks For Geeks on AVL Trees</a>
              <br />
                <a href = "https://www.tutorialspoint.com/data_structures_algorithms/avl_tree_algorithm.htm"> Tutorialspoint on AVL Trees</a>
              <br />
                <a href = "https://en.wikipedia.org/wiki/AVL_tree"> Wikipedia on AVL Trees </a>
              <br /> <br />
          </div>

          <div class="text-center">
              <h2 className="text-center text-gray-600 underline font-bold text-xl" > Videos </h2>
                <div class="items-center inline-flex">
                    <iframe class="p-4" width="450" height="300" src="https://www.youtube.com/embed/5C8bLQBjcDI" frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen></iframe>
                    <iframe class="p-4" width="450" height="300" src="https://www.youtube.com/embed/vRwi_UcZGjU" frameBorder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen></iframe>
                    <iframe class="p-4" width="450" height="300" src="https://www.youtube.com/embed/ygZMI2YIcvk" frameBorder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen></iframe>
                </div>
             </div>
          </div>
      )
    }
  }
  export default Tutorial
