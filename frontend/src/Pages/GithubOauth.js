import React, { useEffect } from 'react'
import { Navigate, useNavigate, useSearchParams } from 'react-router-dom';
import axios from '../HelperFunctions/customAxios';

export default function GithubOauth() {
    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();
    const loginCode = searchParams.get('code'), stateValue = searchParams.get('state');

    const localStorageState = localStorage.getItem('state');
    console.log(localStorageState, stateValue);

    if(localStorageState !== stateValue){
        console.error("State values do not match");
        return (
            <Navigate to="/" />
        );
    }

    useEffect( () => {
        axios.post('/api/github/login', {
            "code": loginCode
        })
        .then (() => {
            navigate('/');
        })
        .catch( (err) => {
            console.error("Failed to handle GitHub login", err);
        });
    }, []);

    return (
    <>
        You are being redirected to Home page...
    </>
    )
}
