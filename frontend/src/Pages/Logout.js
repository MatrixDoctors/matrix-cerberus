import axios from 'axios'
import React, { useContext, useEffect } from 'react'
import { useNavigate } from 'react-router-dom';
import { GlobalContext } from '../GlobalContext';

export default function Logout() {
    const navigate = useNavigate();
    const {setMatrixUserId} = useContext(GlobalContext);
    useEffect( ()=> {
        async function signOutUser() {
            axios.post('api/users/logout')
            .then( (resp) => {
                console.log(resp);
                setMatrixUserId('');
                navigate('/login');
            });
        }
        signOutUser();
    }, [])
    return (
        <>
        </>
    )
}
