import React from 'react'
import Navigation from './Navigation'


function Header(){
    return(
        <header className="border-dotted border-4 border-gray-600 font-bold p-5 flex justify-between ">
        Data Structures Game
        <Navigation />
        </header>
    )   
}
export default Header