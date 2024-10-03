import axios from "axios";

export const fetchEeIndexData = async <T>(data: T) => {
  const response = await axios.post("http://localhost:8000/ee-index", data);
  return response.data;
};

type DownloadData = {
  date: string;
  station: string;
};

export const fetchFile = async (data: DownloadData) => {
  const response = await axios.post(
    "http://localhost:8000/ee-index/download",
    data
  );
  return response.data;
};
