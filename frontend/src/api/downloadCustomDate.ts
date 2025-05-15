import { apiClient } from "./config";

// Request type
export type DownloadCustomDateEeIndexRequest = {
  startDate: string;
  endDate: string;
  stationCode: string;
};

// Response type
export type DownloadCustomDateEeIndexResponse = any;

export const fetchCustomDateFile = async (
  data: DownloadCustomDateEeIndexRequest
): Promise<DownloadCustomDateEeIndexResponse> => {
  const response = await apiClient.get("/download/ee-index", {
    params: data,
  });
  return response.data;
};