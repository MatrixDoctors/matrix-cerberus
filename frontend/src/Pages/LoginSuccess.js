import React from 'react'
import { useSearchParams } from 'react-router-dom'
import axios from 'axios';

export default function LoginSuccess() {
    const [searchParams, setSearchParams] = useSearchParams();
    const loginToken = searchParams.get('loginToken');
    const homeServer = localStorage.getItem('homeServer');
    const fullUrl = new URL('/_matrix/client/v3/login', homeServer);

    async function fetchData(){
        const response = await axios.post(fullUrl, {
            type: "m.login.token",
            token: loginToken
        });
        console.log(response.data);
    }
    fetchData();

    return (
        <div>LoginSuccess</div>
    )
}
