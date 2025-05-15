import {
  fetchEeIndexFromDateWithDays,
  type DownloadDailyDateEeIndexReq,
} from "@/api";

export const downloadFile = async (fileParams: {
  startDate: string;
  days: number;
  stationCode: string;
}) => {
  const { startDate, days, stationCode } = fileParams;

  const req: DownloadDailyDateEeIndexReq = {
    startDate,
    days,
    stationCode,
  };

  const responseData = await fetchEeIndexFromDateWithDays(req);
  const byteCharacters = atob(responseData.file);
  const byteNumbers = new Uint8Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const blob = new Blob([byteNumbers], { type: "application/zip" });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", "ee_index.zip");
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};
