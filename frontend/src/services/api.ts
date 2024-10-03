import axios from "axios";

export const fetchEeIndexData = async <T>(data: T) => {
  const response = await axios.post("http://localhost:8000/ee-index", data);
  return response.data;
};
