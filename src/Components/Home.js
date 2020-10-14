import React from 'react'
import Header from './Header'
import "./styles.css";
import Particles from 'react-particles-js';

function Home(){
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

        <h1 className="font-bold text-2xl"> Home</h1>
    </div>
    )
}
export default Home