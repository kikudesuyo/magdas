import { useState } from "react";
import Button from "@/components/button/Button";
import DownloadButton from "@/features/download/DownloadButton";

type DataSelectorProps = {
  onSelect: (station: string, dataKind: string, date: string) => void;
};

const DataSelector = ({ onSelect }: DataSelectorProps) => {
  const [station, setStation] = useState("ANC");
  const [dataKind, setDataKind] = useState("EE-index");
  const [date, setDate] = useState("2014-06-03");

  const handleSelect = () => {
    if (!date) {
      alert("日時を入力してください");
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

    onSelect(station, dataKind, date);
  };

  return (
    <div className="flex flex-col border bg-slate-50 gap-8 p-4">
      <div>
        <label className="text-sm">観測地点</label>
        <select
          className="border border-gray-300 rounded-md"
          value={station}
          onChange={(e) => setStation(e.target.value)}
        >
          <option value="AAB">AAB</option>
          <option value="ANC">ANC</option>
          <option value="DAV">DAV</option>
          <option value="EUS">EUS</option>
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
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>
      <Button label="プロット" func={handleSelect} />
      <DownloadButton date={date} station={station} />
    </div>
  );
};

export default DataSelector;
