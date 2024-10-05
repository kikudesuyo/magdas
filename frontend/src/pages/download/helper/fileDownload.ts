import { fetchCustomDateFile } from "@/services/api";

export const downloadFile = async (fileParams: {
  startDate: string;
  endDate: string;
  station: string;
}) => {
  const { startDate, endDate, station } = fileParams;
  console.log(startDate, endDate, station);
  const responseData = await fetchCustomDateFile({
    startDate,
    endDate,
    station,
  });
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
