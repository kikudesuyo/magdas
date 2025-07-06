// import { useState, useMemo } from "react";
// import Main from "@/components/Main";
// import EejChart from "@/pages/eej/_components/EejChart";
// import DataRangeSelector from "@/pages/eej/_components/DataSelector";
// import { fetchEejData, type EeJReq, EeJResp } from "@/api";

// const Eej = () => {
//   const [rawData, setRawData] = useState<EeJResp | null>(null);

//   const handleButtonClick = async (
//     startDate: string,
//     days: number,
//     region: string
//   ) => {
//     const reqParams: EeJReq = {
//       startDate,
//       days,
//       region,
//     };
//     const data = await fetchEejData(reqParams);
//     if (!data) return;
//     setRawData(data);
//   };

//   const plotData = useMemo(() => {
//     if (!rawData)
//       return {
//         values: { dipEuel: [], offdipEuel: [] },
//         minuteLabels: [],
//         singularEejDates: [],
//       };
//     return {
//       values: {
//         dipEuel: rawData.data.map((row) => row.dipEuel ?? NaN),
//         offdipEuel: rawData.data.map((row) => row.offdipEuel ?? NaN),
//       },
//       minuteLabels: rawData.data.map((row) => row.time),
//       singularEejDates: rawData.singularEejDates,
//     };
//   }, [rawData]);
//   return (
//     <Main style="items-center gap-8 pt-4">
//       <h1 className="text-4xl font-bold">EEJ Plot</h1>
//       <div className="flex flex-row gap-4">
//         <DataRangeSelector onSelect={handleButtonClick} />
//         <EejChart
//           values={plotData.values}
//           minuteLabels={plotData.minuteLabels}
//           singularEejDates={plotData.singularEejDates}
//         />
//       </div>
//     </Main>
//   );

//   // if (!rawData) {
//   //   return (
//   //     <Main style="items-center gap-8 pt-4">
//   //       <h1 className="text-4xl font-bold">EEJ Plot</h1>
//   //       <DataRangeSelector onSelect={handleButtonClick} />
//   //     </Main>
//   //   );
//   // }

//   // const values = {
//   //   dipEuel: rawData.data.map((row) => row.dipEuel ?? NaN),
//   //   offdipEuel: rawData.data.map((row) => row.offdipEuel ?? NaN),
//   // };
//   // const minuteLabels = rawData.data.map((row) => row.time);
//   // const singularEejDates = rawData.singularEejDates;
//   // console.log("debug:", minuteLabels.length);

//   // return (
//   //   <Main style="items-center gap-8 pt-4">
//   //     <h1 className="text-4xl font-bold">EEJ Plot</h1>
//   //     <div className="flex flex-row gap-4">
//   //       <DataRangeSelector onSelect={handleButtonClick} />
//   //       <EejChart
//   //         values={values}
//   //         minuteLabels={minuteLabels}
//   //         singularEejDates={singularEejDates}
//   //       />
//   //     </div>
//   //   </Main>
//   // );
// };

// export default Eej;

import { useState, useMemo } from "react";
import Main from "@/components/Main";
import EejChart from "@/pages/eej/_components/EejChart";
import DataRangeSelector from "@/pages/eej/_components/DataSelector";
import { fetchEejData, type EeJReq, EeJResp } from "@/api";

const Eej = () => {
  const [rawData, setRawData] = useState<EeJResp | null>(null);

  const handleButtonClick = async (
    startDate: string,
    days: number,
    region: string
  ) => {
    const reqParams: EeJReq = {
      startDate,
      days,
      region,
    };
    const data = await fetchEejData(reqParams);
    if (!data) return;
    setRawData(data);
  };

  const plotData = useMemo(() => {
    if (!rawData) return null; // 🔧 空のオブジェクトではなくnullを返す

    return {
      values: {
        dipEuel: rawData.data.map((row) => row.dipEuel ?? NaN),
        offdipEuel: rawData.data.map((row) => row.offdipEuel ?? NaN),
      },
      minuteLabels: rawData.data.map((row) => row.time),
      singularEejDates: rawData.singularEejDates,
    };
  }, [rawData]);

  // 🎯 データがない場合は早期リターン
  if (!plotData) {
    return (
      <Main style="items-center gap-8 pt-4">
        <h1 className="text-4xl font-bold">EEJ Plot</h1>
        <DataRangeSelector onSelect={handleButtonClick} />
      </Main>
    );
  }

  return (
    <Main style="items-center gap-8 pt-4">
      <h1 className="text-4xl font-bold">EEJ Plot</h1>
      <div className="flex flex-row gap-4">
        <DataRangeSelector onSelect={handleButtonClick} />
        <EejChart
          values={plotData.values}
          minuteLabels={plotData.minuteLabels}
          singularEejDates={plotData.singularEejDates}
        />
      </div>
    </Main>
  );
};

export default Eej;
