import { useState } from "react";
import Button from "@/components/button/Button";
import DownloadButton from "@/pages/ee-index/_components/DownloadButton";
import { STATIONS } from "@/utils/constant";

type DataSelectorProps = {
  onSelect: (station: string, startDate: string, days: number) => void;
};

const DAYS_OPTIONS = [
  { value: 1, label: "1 day" },
  { value: 3, label: "3 days" },
  { value: 7, label: "7 days" },
  { value: 30, label: "30 days" },
];

const DEFAULT_DAYS = 1;

const DataRangeSelector = ({ onSelect }: DataSelectorProps) => {
  const [startDate, setStartDate] = useState("2014-06-03");
  const [days, setDays] = useState(DEFAULT_DAYS);
  const [station, setStation] = useState("ANC");

  const handleSelect = () => {
    if (!startDate) {
      alert("開始日時を入力してください");
      return;
    }

    if (!station) {
      alert("観測地点を選択してください");
      return;
    }

    onSelect(station, startDate, days);
  };

  return (
    <div className="flex flex-col border bg-slate-50 gap-8 p-4">
      <div>
        <label className="text-sm">観測地点</label>
        <select
          value={station}
          onChange={(e) => setStation(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          {STATIONS.map((station) => (
            <option key={station} value={station}>
              {station}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label className="text-sm">開始日時</label>
        <input
          type="date"
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
      </div>
      <div>
        <label className="text-sm">表示日数</label>
        <select
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          {DAYS_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      <Button label="プロット" func={handleSelect} />
      <DownloadButton startDate={startDate} days={days} stationCode={station} />
    </div>
  );
};

export default DataRangeSelector;
