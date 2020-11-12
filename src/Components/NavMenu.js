import React, { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars } from '@fortawesome/free-solid-svg-icons'

//this child component is called in Header compoment to be displayed on every page
function NavMenu(){
    //react hook to click and expand/minimize menu
    //conditional rendering:show html only when state is true

    const [showMenu, setShowMenu] = useState(false)

    //MENU initialized to null
    //MASKMENU toggles the menu to visible/invisible when menu button is clicked
    let menu
    let menuMask
    if(showMenu){
        menu= <div
        className="fixed bg-red-600 top-0 right-0 w-1/6 h-full z-50 shadow"
        > 
        <div class="dropdown">
  
  <ul class='nav-links'>
        <li>
            <a className="text-gray-100 py-3 border-t border-b block" href='/'>Home</a>
        </li>
        <li>
            <a className="text-gray-100 py-3 border-t border-b block" href='/game_board'>Game</a>
        </li>
        <li>
            <a className="text-gray-100 py-3 border-t border-b block" href='/profile_page'>Profile & Login</a>
        </li>
  </ul>
</div>
        </div>
        
        menuMask=
        <div className="bg-black-t-50 fixed top-0 left-0 w-full h-full z-50"
            onClick={() => setShowMenu(false)}
        >  

        </div>
    }
    //import icon and toggle menu when icon is clicked via react hooks
    return(
        <header>
        <nav>
           
                <FontAwesomeIcon 
                icon={faBars} size="lg"
                onClick={() => setShowMenu(!showMenu)}
                />
            
            {menuMask}
            {menu}
        </nav>
        </header>
    )
}
export default NavMenu


