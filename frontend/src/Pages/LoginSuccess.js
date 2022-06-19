import React from 'react'
import { useSearchParams } from 'react-router-dom'
import axios from 'axios';
import { MatrixApi } from '../MatrixApi';

/**
 * This page is sent as a redirectUrl parameter when a request is sent to the '/login/sso/rediect/ endpoint.
 * It handles the rest of the workflow after the user is redirected to this page with a login token as a query parameter.
 * For more information refer to https://spec.matrix.org/latest/client-server-api/#client-login-via-sso
 */
export default function LoginSuccess() {
    const [searchParams, setSearchParams] = useSearchParams();
    const loginToken = searchParams.get('loginToken');
    const homeServer = localStorage.getItem('homeServer');

    async function fetchData(){
        const response = await new MatrixApi(homeServer).login('POST', {
            type: "m.login.token",
            token: loginToken
        })
    }
    fetchData();

    return (
        <div>LoginSuccess</div>
    )
}
