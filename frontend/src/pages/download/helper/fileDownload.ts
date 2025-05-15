import { fetchCustomDateFile, type DownloadCustomDateEeIndexReq } from "@/api";

export const downloadFile = async (fileParams: {
  startDate: string;
  endDate: string;
  stationCode: string;
}) => {
  const { startDate, endDate, stationCode } = fileParams;

  const req: DownloadCustomDateEeIndexReq = {
    startDate,
    endDate,
    stationCode,
  };

  const resp = await fetchCustomDateFile(req);
  const byteCharacters = atob(resp.base64Zip);
  const byteNumbers = new Uint8Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const blob = new Blob([byteNumbers], { type: resp.contentType });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", resp.fileName);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};
