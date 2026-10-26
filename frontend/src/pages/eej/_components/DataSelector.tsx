import { useState } from "react";
import Button from "@/components/button/Button";
import { STATIONS } from "@/utils/constant";

type DataSelectorProps = {
  onSelect: (startDate: string, days: number, stations: string) => void;
};

type Station = (typeof STATIONS)[number];

type StationPreset = {
  label: string;
  stations: Station[];
};

const STATION_PRESETS: StationPreset[] = [
  {
    label: "South America (ANC,HUA,EUS)",
    stations: ["ANC", "EUS"],
  },
];

const DAYS_OPTIONS = [
  { value: 1, label: "1 day" },
  { value: 3, label: "3 days" },
  { value: 7, label: "7 days" },
  { value: 30, label: "30 days" },
];

const DEFAULT_DAYS = 3;

const DataRangeSelector = ({ onSelect }: DataSelectorProps) => {
  const [startDate, setStartDate] = useState("2020-02-22");
  const [days, setDays] = useState(DEFAULT_DAYS);
  const [stations, setStations] = useState(
    STATION_PRESETS[0].stations.join(",")
  );

  const handleSelect = () => {
    if (!startDate) {
      alert("開始日時を入力してください");
      return;
    }
    if (!stations) {
      alert("観測地点を選択してください");
      return;
    }
    onSelect(startDate, days, stations);
  };

  return (
    <div className="flex flex-col border bg-slate-50 gap-8 p-4">
      <div>
        <label className="text-sm">観測地点</label>
        <select
          value={stations}
          onChange={(e) => setStations(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          {STATION_PRESETS.map((preset) => {
            const value = preset.stations.join(",");
            return (
              <option key={value} value={value}>
                {preset.label}
              </option>
            );
          })}
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
    </div>
  );
};

export default DataRangeSelector;
