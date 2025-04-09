import { useState } from "react";
import { downloadFile } from "@/pages/ee-index/helper/fileDownload";

type DailyDownloadData = {
  date: string;
  stationCode: string;
};
const DownloadButton = ({ date, stationCode }: DailyDownloadData) => {
  const [loading, setLoading] = useState(false);
  const handleDownload = async () => {
    setLoading(true);

    try {
      await downloadFile({
        date: date,
        stationCode: stationCode,
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
