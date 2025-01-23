import { useState } from "react";
import Button from "@/components/button/Button";
import DownloadButton from "@/pages/ee-index/_components/DownloadButton";
import { STATIONS } from "@/utils/constant";

type DataSelectorProps = {
  onSelect: (station: string, dataKind: string, date: string) => void;
};

const DataRangeSelector = ({ onSelect }: DataSelectorProps) => {
  const [station, setStation] = useState("ANC");
  const [dataKind, setDataKind] = useState("EE-index");
  const [startDate, setStartDate] = useState("2014-06-03");
  const [endDate, setEndDate] = useState("2014-06-10");

  const handleSelect = () => {
    if (!startDate) {
      alert("開始日時を入力してください");
      return;
    }
    if (!endDate) {
      alert("終了日時を入力してください");
      return;
    }

    if (!dataKind) {
      alert("データ種別を選択してください");
      return;
    }
    if (!station) {
      alert("観測地点を選択してください");
      return;
    }

    onSelect(station, dataKind, startDate);
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
        <label className="text-sm">データ種別</label>
        <select
          className="border border-gray-300 rounded-md"
          value={dataKind}
          onChange={(e) => setDataKind(e.target.value)}
        >
          <option value="EE-index">EE-index</option>
        </select>
      </div>
      <div>
        <label className="text-sm">開始日時</label>
        <input
          type="date"
          className="border border-gray-300 rounded-md"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
      </div>
      <div>
        <label className="text-sm">終了日時</label>
        <input
          type="date"
          className="border border-gray-300 rounded-md"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </div>
      <Button label="プロット" func={handleSelect} />
      <DownloadButton
        startDate={startDate}
        endDate={endDate}
        station={station}
      />
    </div>
  );
};

export default DataRangeSelector;
