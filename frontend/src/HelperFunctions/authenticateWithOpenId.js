import axios from 'axios';
import React from 'react'
import { useNavigate } from 'react-router-dom'
import validateAndReturnUrl from './validateAndReturnUrl';

export default async function authenticateWithOpenId(responseDetails, backendServer) {
  const baseUrl = validateAndReturnUrl(responseDetails.home_server);
  const endpoint = `/_matrix/client/v3/user/${responseDetails.user_id}/openid/request_token`
  const fullUrl = new URL(endpoint, baseUrl);

  const response = await axios.post(fullUrl, {}, {
    headers: {
      'Authorization': `Bearer ${responseDetails.access_token}`
    }
  })
  console.log(response.data);
  // const navigate = useNavigate();
  // navigate('/');
}
