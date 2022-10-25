import React, { useEffect } from 'react'
import { Navigate, useNavigate, useSearchParams } from 'react-router-dom';
import PropTypes from "prop-types"
import axios from '../HelperFunctions/customAxios';

export default function OAuth({accountType}) {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const loginCode = searchParams.get('code'), stateValue = searchParams.get('state');

    const localStorageState = localStorage.getItem('state');

    if(localStorageState !== stateValue){
        console.error("State values do not match");
        return (
            <Navigate to="/" />
        );
    }

    useEffect( () => {
        axios.post(`/api/${accountType}/login`, {
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

OAuth.propTypes = {
    accountType: PropTypes.string
}
