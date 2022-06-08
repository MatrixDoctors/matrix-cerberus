import React, { useState } from 'react'
import { Link } from 'react-router-dom'

export default function AccountDropdown() {
    const [isAccountDropdownOpen, setIsAccountDropdownOpen] = useState(false);

    function handleClick(){
        setIsAccountDropdownOpen(!isAccountDropdownOpen);
    }

    let accountOptionsDisplay = `${isAccountDropdownOpen ? "block" : "hidden"}`;

    return (
    <div className="hidden sm:block mt-2 sm:ml-6">
        <div className='relative'>
            <button onClick={handleClick} className='block h-6 w-6 overflow-hidden rounded-full mr-2 mb-1 border-2 border-gray-600 hover:border-gray-50'>
                <img className='h-full w-full object-cover' src='https://images.unsplash.com/photo-1531427186611-ecfd6d936c79?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80' />
            </button>
            
            <div className={accountOptionsDisplay}>
                <button onClick={()=>{setIsAccountDropdownOpen(false)}} className="fixed top-0 left-0 right-0 bottom-0 h-full w-full bg-black opacity-50"></button>
                <div className='absolute right-0 mt-1 w-32 py-2 bg-white rounded-lg shadow-xl'>
                    <Link to='/login' onClick={()=>{setIsAccountDropdownOpen(false)}} className='block px-2 py-2 text-gray-800 hover:bg-indigo-500 hover:text-white'>Login</Link>
                    <Link to='/logout' onClick={()=>{setIsAccountDropdownOpen(false)}} className='block px-2 py-2 text-gray-800 hover:bg-indigo-500 hover:text-white'>Sign Out</Link>
                </div>
            </div>
        </div>
    </div>
    )
}
