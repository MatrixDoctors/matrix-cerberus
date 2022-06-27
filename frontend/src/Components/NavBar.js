import React, { useContext, useState } from 'react'
import { Link } from 'react-router-dom'
import { GlobalContext } from '../GlobalContext';
import AccountDropdown from './AccountDropdown';

export default function NavBar() {
    const [isOpen, setIsOpen] = useState(false);
    const {matrixUserId, setMatrixUserId} = useContext(GlobalContext);

    function handleClick() {
        setIsOpen(!isOpen);
    }

    let contentDisplay = `${isOpen ? "block" : "hidden"} sm:block`;

    return (
    <nav className="sm:flex sm:justify-between sm:items-center sm:px-4 sm:py-2 bg-dark-ash">
        <div className='flex items-center justify-between px-4 py-2 sm:p-0'>
            <div className="text-white font-bold">
                <Link to='/'>matrix-cerberus</Link>
            </div>
            <div className='sm:hidden'>
                <button onClick={handleClick} className="block">
                    <svg className="h-4 w-4 fill-current"
                        viewBox='0 0 10 8' width='40'>
                        <path d='M1 1h8M1 4h 8M1 7h8' stroke='#a0aec0' strokeWidth='2' strokeLinecap='round'/>
                    </svg>
                </button>
            </div>
        </div>

        <div className={contentDisplay}>
            <div>
                <div className='px-4 pt-2 pb-4 sm:flex sm:items-center'>
                    <Link to='/' className="block mt-1 py-1 sm:px-2 sm:ml-2 font-semibold rounded text-gray-300 hover:bg-gray-800 focus:text-white">Accounts</Link>
                    <Link to='/room-settings' className="block mt-1 py-1 sm:px-2 sm:ml-2 font-semibold rounded text-gray-300 hover:bg-gray-800 focus:text-white">Room Settings</Link>
                    <Link to='/server-settings' className="block mt-1 py-1 sm:px-2 sm:ml-2 font-semibold rounded text-gray-300 hover:bg-gray-800 focus:text-white">Server Settings</Link>
                    {/* Account dropdown for desktop views */}
                    <AccountDropdown/>
                </div>

                {/* Account dropdown for mobile views */}
                <div className='px-4 py-5 border-t border-gray-800 sm:hidden'>
                    <div className='mb-3 flex items-center'>
                        <img alt="..." className='h-6 w-6 border-2 border-gray-600 rounded-full object-cover' src={require('../assets/img/user.svg').default} />
                        <span className='ml-3 font-semibold text-white'>kuries</span>
                    </div>
                    <Link to='/login' className='block mt-2 text-gray-400 hover:text-white'>Log in</Link>
                    <Link to='/logout' className='block mt-2 text-gray-400 hover:text-white'>Sign Out</Link>
                </div>
            </div>
        </div>
    </nav>
    )
}
