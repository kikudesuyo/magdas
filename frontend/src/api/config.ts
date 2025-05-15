import axios from "axios";

export const apiURL = "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: apiURL,
});