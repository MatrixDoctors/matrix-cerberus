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
        async function sendCode(){
            await axios.post('api/github/login', {
                "code": loginCode
            })
            .catch( (err) => {
                console.error(err);
            });
        }
        const resp = sendCode();
        resp.then( (resp) => {
            navigate('/');
        });
    });
    return (
    <></>
    )
}
