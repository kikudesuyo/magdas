import { useState } from "react";
import Main from "@/components/Main";
import EeIndexChart from "@/pages/ee-index/_components/EeIndexChart";
import DataRangeSelector from "@/pages/ee-index/_components/DataSelector";
import { fetchEeIndexData, type EeIndexResp, type EeIndexReq } from "@/api";

const EeIndex = () => {
  const [plotData, setPlotData] = useState<EeIndexResp>({
    values: { er: [], edst: [], euel: [] },
    minuteLabels: [],
  });

  const handleButtonClick = async (
    stationCode: string,
    startDate: string,
    days: number
  ) => {
    const reqParams: EeIndexReq = {
      startDate,
      days,
      stationCode,
    };
    const data = await fetchEeIndexData(reqParams);
    if (!data) return;
    setPlotData(data);
  };

  return (
    <Main style="items-center gap-8 pt-4">
      <h1 className="text-4xl font-bold">EE-index Plot</h1>
      <div className="flex flex-row gap-4">
        <DataRangeSelector onSelect={handleButtonClick} />
        <EeIndexChart
          values={plotData.values}
          minuteLabels={plotData.minuteLabels}
        />
      </div>
    </Main>
  );
};

export default EeIndex;
