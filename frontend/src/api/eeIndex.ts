import { apiClient } from "./config";

export type EeIndexReq = {
  startDate: string;
  days: number;
  stationCode: string;
};

export type EeIndexResp = {
  values: {
    er: number[];
    edst: number[];
    euel: number[];
  };
  minuteLabels: string[];
};

export const fetchEeIndexData = async (
  req: EeIndexReq
): Promise<EeIndexResp> => {
  const resp = await apiClient.get("/ee-index", {
    params: req,
  });
  return resp.data;
};
