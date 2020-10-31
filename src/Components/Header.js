import React from 'react'
import NavMenu from './NavMenu';
//header component called in every page and displays its child component to display the menu
function Header(){
    return(
<header className="border-b p-3 flex justify-between items-center">
        Data Structures Game

    <NavMenu />
        </header>

        
    )   
}
export default Header