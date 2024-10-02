// src/axiosInstance.js
import axios from "axios";

const axiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL, // 기본 URL 설정
});

export default axiosInstance;
