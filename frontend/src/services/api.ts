import axios from "axios";

const apiURL = "http://localhost:8000";

export const fetchEeIndexData = async <T>(data: T) => {
  const response = await axios.get(`${apiURL}/ee-index`, {
    params: data,
  });
  return response.data;
};

type DownloadCustomDateEeIndex = {
  startDate: string;
  endDate: string;
  station: string;
};

export const fetchCustomDateFile = async (data: DownloadCustomDateEeIndex) => {
  const response = await axios.get(`${apiURL}/download/ee-index`, {
    params: data,
  });
  return response.data;
};

type DownloadDailyDateEeIndex = {
  date: string;
  station: string;
};

export const fetchDailyDateFile = async (data: DownloadDailyDateEeIndex) => {
  const response = await axios.get(`${apiURL}/download/ee-index/daily`, {
    params: data,
  });
  return response.data;
};
