import { apiClient } from "./config";

export type DownloadEeIndexByRangeReq = {
  startDate: string;
  endDate: string;
  stationCode: string;
};

export type DownloadEeIndexByRangeResp = {
  base64Zip: string;
  fileName: string;
  contentType: string;
};

export const fetchCustomDateFile = async (
  req: DownloadEeIndexByRangeReq
): Promise<DownloadEeIndexByRangeResp> => {
  const resp = await apiClient.get("/download/ee-index/by-range", {
    params: req,
  });
  return resp.data;
};
