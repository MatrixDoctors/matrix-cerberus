import axios from 'axios';

export default async function authenticateWithOpenId(responseDetails) {
  const baseUrl = localStorage.getItem('homeServer');
  const endpoint = `/_matrix/client/v3/user/${responseDetails.user_id}/openid/request_token`
  const fullUrl = new URL(endpoint, baseUrl);

  const response = await axios.post(fullUrl, {}, {
    headers: {
      'Authorization': `Bearer ${responseDetails.access_token}`
    }
  })

  await axios.post("/api/users/verify-openid", response.data)
  .then( (resp) => {
    console.log(resp.data);
  });
}
