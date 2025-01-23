import { useState } from "react";
import { downloadFile } from "@/pages/ee-index/helper/fileDownload";

type DownloadData = {
  startDate: string;
  endDate: string;
  station: string;
};
const DownloadButton = ({ startDate, endDate, station }: DownloadData) => {
  const [loading, setLoading] = useState(false);
  const handleDownload = async () => {
    setLoading(true);

    try {
      await downloadFile({
        startDate: startDate,
        endDate: endDate,
        station: station,
      });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleDownload}
      disabled={loading}
      className="bg-blue-500 text-white py-2 px-4 rounded"
    >
      {loading ? "ダウンロード中..." : "ダウンロード"}
    </button>
  );
};

export default DownloadButton;
