import { useState } from "react";
import { downloadFile } from "@/pages/ee-index/helper/fileDownload";

type DailyDownloadData = {
  startDate: string;
  days: number;
  stationCode: string;
};
const DownloadButton = ({
  startDate,
  days,
  stationCode,
}: DailyDownloadData) => {
  const [loading, setLoading] = useState(false);
  const handleDownload = async () => {
    setLoading(true);

    try {
      await downloadFile({
        startDate,
        days,
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
