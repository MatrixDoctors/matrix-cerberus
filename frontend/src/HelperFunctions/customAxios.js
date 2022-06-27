import axios from "axios";
import history from "./customHistory";

const axiosInstance = axios.create();

axiosInstance.interceptors.response.use(
  function (response) {
    return response;
  },
  function (err) {
    if (axios.isAxiosError(err) && err.response?.status == 401 ) {
      console.error("Unauthorized request to server, redirecting to /login", err);
      history.replace("/login");
    }

    return Promise.reject(err);
  }
);

export default axiosInstance;
