import { STATIONS } from "@/utils/constant";

const StationSelect = (station: string) => {
  return (
    <select
      className="border border-gray-300 rounded-md"
      value={station}
      defaultValue={station}
    >
      {STATIONS.map((station) => (
        <option key={station} value={station}>
          {station}
        </option>
      ))}
    </select>
  );
};

export default StationSelect;
