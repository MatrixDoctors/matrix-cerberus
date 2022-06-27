import axios from 'axios';
import { MatrixApi } from '../MatrixApi';

export default async function authenticateWithOpenId(responseDetails) {
  const baseUrl = localStorage.getItem('homeServer');

  const response = await new MatrixApi().requestOpenIdToken('POST', baseUrl, responseDetails);

  await axios.post("/api/users/verify-openid", response.data)
  .then( (resp) => {
    console.log(resp.data);
  });
}
