import { apiClient } from "./config";

export type EeJReq = {
  startDate: string;
  days: number;
  region: "south-america" | string;
};

type EejRow = {
  time: string;
  dipEuel: number | null;
  offdipEuel: number | null;
};

export type EeJResp = {
  data: EejRow[];
  peculiarEejDates: string[];
};

export const fetchEejData = async (req: EeJReq): Promise<EeJResp> => {
  const resp = await apiClient.get("/eej", {
    params: req,
  });
  return resp.data;
};
