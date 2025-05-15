import { apiClient } from "./config";

export type DownloadCustomDateEeIndexReq = {
  startDate: string;
  endDate: string;
  stationCode: string;
};

export type DownloadCustomDateEeIndexResp = {
  base64Zip: string;
  fileName: string;
  contentType: string;
};

export const fetchCustomDateFile = async (
  req: DownloadCustomDateEeIndexReq
): Promise<DownloadCustomDateEeIndexResp> => {
  const resp = await apiClient.get("/download/ee-index", {
    params: req,
  });
  return resp.data;
};
