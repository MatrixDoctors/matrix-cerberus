import axios from "axios";
import history from "./customHistory";
import 'react-toastify/dist/ReactToastify.css';
import { toast } from "react-toastify";

const axiosInstance = axios.create({baseURL: "http://localhost:80"});

axiosInstance.interceptors.response.use(
  function (response) {
    return response;
  },
  function (err) {
    const regexForServerErrorCodes = /5[0-9][0-9]/;

    if (axios.isAxiosError(err) && err.response?.status == 401 ) {
      history.replace("/login");
      console.error("Unauthorized request to server, redirecting to /login");
      toast.error("User not logged in.");
    }

    if (axios.isAxiosError(err) && err.response?.status == 502) {
      toast.error("Cannot connect with the server.");
    }

    return Promise.reject(err);
  }
);

export default axiosInstance;
