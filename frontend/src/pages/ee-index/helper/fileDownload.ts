import { fetchFile } from "@/services/api";

export const downloadFile = async (fileParams: {
  date: string;
  station: string;
}) => {
  const { date, station } = fileParams;
  const responseData = await fetchFile({
    date,
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
