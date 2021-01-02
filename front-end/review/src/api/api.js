
import axios from "axios";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "https://api.video-review.top:1314/api/";
axios.defaults.headers.post["Content-Type"] = "application/json";

export const  requestLogin = async params => { return await axios.post(`login/`, params).then(res => res.data); };

