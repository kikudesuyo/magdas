import axios from "axios";

const apiURL = import.meta.env.VITE_API_URL;

if (!apiURL) {
  throw new Error("VITE_API_URL is not set. Please check your .env file.");
}

export const apiClient = axios.create({
  baseURL: apiURL,
});
