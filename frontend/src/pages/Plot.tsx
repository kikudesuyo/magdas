import { useState } from "react";
import Main from "@/components/Main";
import EeIndexChart from "@/features/chart/EeIndexChart";
import DataSelector from "@/features/chart/DataRangeSelector";
import { fetchEeIndexData } from "@/services/api";

type ResParams = {
  values: {
    er: number[];
    edst: number[];
    euel: number[];
  };
  date: string;
};

const Plot = () => {
  const [plotData, setPlotData] = useState<ResParams>({
    values: { er: [], edst: [], euel: [] },
    date: "",
  });

  const handleButtonClick = async (
    station: string,
    dataKind: string,
    date: string
  ) => {
    const reqParams = { station, dataKind, date };
    const data = await fetchEeIndexData(reqParams);
    if (!data) return;
    setPlotData(data);
  };

  return (
    <Main style="items-center gap-8 pt-4">
      <h1 className="text-4xl">EE-indexのプロット</h1>
      <div className="flex flex-row gap-4">
        <DataSelector onSelect={handleButtonClick} />
        <EeIndexChart values={plotData.values} date={plotData.date} />
      </div>
    </Main>
  );
};

export default Plot;
