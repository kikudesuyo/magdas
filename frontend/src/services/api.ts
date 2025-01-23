import axios from "axios";

// const apiURL = process.env.VITE_REACT_APP_API_BASE_URL;
const apiURL = "http://localhost:8000";

export const fetchEeIndexData = async <T>(data: T) => {
  const response = await axios.post(`${apiURL}/ee-index`, data);
  return response.data;
};

type DownloadCustomDateEeIndex = {
  startDate: string;
  endDate: string;
  station: string;
};

export const fetchCustomDateFile = async (data: DownloadCustomDateEeIndex) => {
  const response = await axios.post(`${apiURL}/download/ee-index`, data);
  return response.data;
};
