import axios from "axios";

const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_URL, // Vite에서 환경 변수 사용
});

export default axiosInstance;