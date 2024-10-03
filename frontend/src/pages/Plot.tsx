import { useState } from "react";
import Main from "@/components/Main";
import EeIndexChart from "@/components/chart/EeIndexChart";
// import StationSelect from "@/components/StationSelect";
import Button from "@/components/Button";
import { fetchEeIndexData } from "@/services/api";

type ResParams = {
  values: {
    er: number[];
    edst: number[];
    euel: number[];
  };
};

const Plot = () => {
  const [plotData, setPlotData] = useState<ResParams>({
    values: { er: [], edst: [], euel: [] },
  });
  const [date, setDate] = useState("2014-06-03");
  const [dataKind, setDataKind] = useState("EE-index");
  const [station, setStation] = useState("ANC");

  const reqParams = {
    date,
    dataKind,
    station: station,
  };

  const fetchData = async () => {
    if (date === "") {
      alert("日時を入力してください");
      return;
    }
    if (dataKind === "") {
      alert("データ種別を選択してください");
      return;
    }
    if (station === "") {
      alert("観測地点を選択してください");
      return;
    }

    return await fetchEeIndexData(reqParams);
  };

  const handleButtonClick = async () => {
    const data = await fetchData();
    if (!data) return;
    setPlotData(data);
  };
  return (
    <Main style="items-center gap-8 pt-4">
      <p className="text-4xl">EE-indexのプロット</p>
      <div className="flex flex-row border gap-8">
        {/* 条件入力欄開始 */}
        <div className="flex flex-col border bg-slate-50 gap-8">
          <div>
            <label className="text-sm">観測地点</label>
            {/* <StationSelect onSelectStation={undefined} /> */}
            <select
              className="border border-gray-300 rounded-md"
              value={station}
              onChange={(e) => setStation(e.target.value)}
              defaultValue={station}
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
              defaultValue={dataKind}
            >
              <option value="EE-index">EE-index</option>
              {/* <option value="ER">ER</option>
              <option value="EE">EE</option> */}
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
          <Button
            label="プロット"
            func={async () => {
              await handleButtonClick();
            }}
          />
        </div>
        {/* 条件入力欄終了 */}
        <EeIndexChart values={plotData.values} date={date} />
      </div>
    </Main>
  );
};
export default Plot;
