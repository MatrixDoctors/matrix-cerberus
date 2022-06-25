import axios from "axios";
import history from "./customHistory";

const axiosInstance = axios.create();

axiosInstance.interceptors.response.use(
  function (response) {
    return response;
  },
  function (er) {
    if (axios.isAxiosError(er)) {
      if (er.response) {
        if (er.response.status == 401) {
          history.replace("/login");
        }
      }
    }

    return Promise.reject(er);
  }
);

export default axiosInstance;
