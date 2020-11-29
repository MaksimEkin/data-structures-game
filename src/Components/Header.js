import React from 'react'
import NavMenu from './NavMenu';
//header component called in every page and displays its child component to display the menu
function Header(){
    return(
<header className="border-b p-3 flex justify-between items-center">
    <div className="space-y-10 flex justify-center">
              <h1 className="space-y-5 text-3xl text-center font-semibold text-gray-800 mb-2">Data Structures Game</h1>
    </div>

    <NavMenu />
        </header>

        
    )   
}
export default Header