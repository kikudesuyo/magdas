import { apiClient } from "./config";

// Request type
export type DownloadDailyDateEeIndexRequest = {
  date: string;
  stationCode: string;
};

// Response type
export type DownloadDailyDateEeIndexResponse = any;

export const fetchDailyDateFile = async (
  data: DownloadDailyDateEeIndexRequest
): Promise<DownloadDailyDateEeIndexResponse> => {
  const response = await apiClient.get("/download/ee-index/daily", {
    params: data,
  });
  return response.data;
};