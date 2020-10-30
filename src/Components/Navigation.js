import React, { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars } from '@fortawesome/free-solid-svg-icons'


function Navigation(){
    //react hook to click and expand/minimize menu
    //conditional rendering:show html only when state is true
    
    const [showMenu, setShowMenu] = useState(false)
    //MENU initialized to null
    let menu
    let menuMask
    if(showMenu){
        menu= <div
        className="fixed bg-red-600 top-0 right-0 w-1/5 h-full z-50 shadow"
        > 
        MENU 
        </div>
        
        menuMask=
        <div className="bg-black-t-50 fixed top-0 left-0 w-full h-full z-50"
            onClick={() => setShowMenu(false)}
        >  

        </div>
    }

    return(
        <nav>
            <span >
                <FontAwesomeIcon className="self-end"
                icon={faBars} 
                onClick={() => setShowMenu(!showMenu)}
                />
            </span>
            {menuMask}
            {menu}
        </nav>
    )
}
export default Navigation