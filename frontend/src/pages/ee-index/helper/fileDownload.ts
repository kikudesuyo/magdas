import {
  fetchEeIndexFromDateWithDays,
  type DownloadByDateRangeReq,
} from "@/api";

export const downloadFile = async (fileParams: {
  startDate: string;
  days: number;
  stationCode: string;
}) => {
  const { startDate, days, stationCode } = fileParams;

  const req: DownloadByDateRangeReq = {
    startDate,
    days,
    stationCode,
  };

  const responseData = await fetchEeIndexFromDateWithDays(req);
  const byteCharacters = atob(responseData.base64Zip);
  const byteNumbers = new Uint8Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const blob = new Blob([byteNumbers], { type: responseData.contentType });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", responseData.fileName);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};
