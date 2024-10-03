import { useState } from "react";
import { STATIONS } from "@/utils/constant";

const StationSelect = () => {
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
