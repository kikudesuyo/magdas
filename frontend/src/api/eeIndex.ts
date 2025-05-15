import { apiClient } from "./config";

// Request type
export type EeIndexRequest<T> = T;

// Response type (generic for now, can be updated with actual response structure)
export type EeIndexResponse = any;

export const fetchEeIndexData = async <T>(data: EeIndexRequest<T>): Promise<EeIndexResponse> => {
  const response = await apiClient.get("/ee-index", {
    params: data,
  });
  return response.data;
};