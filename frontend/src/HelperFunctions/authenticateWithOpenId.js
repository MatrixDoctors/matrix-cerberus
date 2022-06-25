import { MatrixApi } from '../MatrixApi';
import axios from "./customAxios";

export default async function authenticateWithOpenId(responseDetails) {
  const baseUrl = localStorage.getItem('homeServer');

  const response = await new MatrixApi().requestOpenIdToken('POST', baseUrl, responseDetails);

  await axios.post("/api/verify-openid", response.data)
  .then( (resp) => {
    console.log(resp.data);
  });
}
