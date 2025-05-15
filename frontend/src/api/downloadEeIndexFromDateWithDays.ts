import { apiClient } from "./config";

export type DownloadByDateRangeReq = {
  startDate: string;
  days: number;
  stationCode: string;
};

export type EeIndexDownloadByDateRangeResp = {
  base64Zip: string;
  fileName: string;
  contentType: string;
};

export const fetchEeIndexFromDateWithDays = async (
  data: DownloadByDateRangeReq
): Promise<EeIndexDownloadByDateRangeResp> => {
  const response = await apiClient.get("/download/ee-index/daily", {
    params: data,
  });
  return response.data;
};
