import React, { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { MatrixApi } from '../MatrixApi';
import authenticateWithOpenId from "../HelperFunctions/authenticateWithOpenId"

/**
 * This page is sent as a redirectUrl parameter when a request is sent to the '/login/sso/rediect/ endpoint.
 * It handles the rest of the workflow after the user is redirected to this page with a login token as a query parameter.
 * For more information refer to https://spec.matrix.org/latest/client-server-api/#client-login-via-sso
 */
export default function LoginSuccess() {
    const [searchParams, setSearchParams] = useSearchParams();
    const loginToken = searchParams.get('loginToken');
    const homeServer = localStorage.getItem('homeServer');
    const navigate = useNavigate();

    useEffect( () => {
        async function fetchData(){
            const response = await new MatrixApi(homeServer).postLogin({
                type: "m.login.token",
                token: loginToken
            });
            await authenticateWithOpenId(response.data);
        }
        try {
            if(loginToken == null){
                throw new Error("Invalid login token.");
            }
            const response = fetchData();
            response.then( ()=>{
                navigate('/');
            });
        }
        catch (err) {
            navigate('/login');
        }
    }, []);

    return (
        <></>
    )
}
