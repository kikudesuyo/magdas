// import Chart from "@/components/chart/Chart";

// type IndexProps = {
//   values: {
//     dipEuel: number[];
//     offdipEuel: number[];
//   };
//   minuteLabels: string[];
//   singularEejDates: string[];
// };

// const EejChart = ({ values, minuteLabels }: IndexProps) => {
//   const { dipEuel, offdipEuel } = values;

//   return (
//     <Chart
//       xLabels={minuteLabels}
//       datasets={[
//         {
//           type: "line",
//           label: "dip",
//           data: dipEuel,
//           borderColor: "blue",
//           tension: 0.2,
//           pointRadius: 0,
//         },
//         {
//           type: "line",
//           label: "offdip",
//           data: offdipEuel,
//           borderColor: "red",
//           tension: 0.2,
//           pointRadius: 0,
//         },
//       ]}
//       xAxisTitle="UT Time"
//       yAxisTitle="nT"
//     />
//   );
// };
// export default EejChart;

import { Plugin } from "chart.js";
import Chart from "@/components/chart/Chart";

type IndexProps = {
  values: {
    dipEuel: number[];
    offdipEuel: number[];
  };
  minuteLabels: string[];
  singularEejDates: string[];
};

const EejChart = ({ values, minuteLabels, singularEejDates }: IndexProps) => {
  const { dipEuel, offdipEuel } = values;

  console.log(singularEejDates);
  const backgroundPlugin: Plugin<"line"> = {
    id: "backgroundPlugin",
    beforeDatasetsDraw(chart) {
      const ctx = chart.ctx;
      const xAxis = chart.scales["x"];

      singularEejDates.forEach((dateStr) => {
        const startIndex = minuteLabels.findIndex((label) =>
          label.startsWith(dateStr)
        );
        if (startIndex === -1) return;

        let endIndex = startIndex;
        for (let i = startIndex; i < minuteLabels.length; i++) {
          if (!minuteLabels[i].startsWith(dateStr)) {
            endIndex = i - 1;
            break;
          }
        }
        if (endIndex < startIndex) endIndex = minuteLabels.length - 1;

        // 修正: ラベルの文字列を渡す
        const startX = xAxis.getPixelForValue(startIndex);
        const endX = xAxis.getPixelForValue(endIndex);

        const topY = chart.chartArea.top;
        const bottomY = chart.chartArea.bottom;

        ctx.save();
        ctx.fillStyle = "rgba(255, 165, 120)";
        ctx.fillRect(startX, topY, endX - startX, bottomY - topY);
        ctx.restore();
      });
    },
  };

  // const backgroundPlugin: Plugin<"line"> = {
  //   id: "backgroundPlugin",
  //   beforeDatasetsDraw(chart) {
  //     const ctx = chart.ctx;
  //     const xAxis = chart.scales["x"];

  //     singularEejDates.forEach((dateStr) => {
  //       // その日の最初のindexをminuteLabelsから探す
  //       const startIndex = minuteLabels.findIndex((label) =>
  //         label.startsWith(dateStr)
  //       );
  //       if (startIndex === -1) return;

  //       // その日の終わりのindex
  //       let endIndex = startIndex;
  //       for (let i = startIndex; i < minuteLabels.length; i++) {
  //         if (!minuteLabels[i].startsWith(dateStr)) {
  //           endIndex = i - 1;
  //           break;
  //         }
  //       }
  //       if (endIndex < startIndex) endIndex = minuteLabels.length - 1;

  //       const startX = xAxis.getPixelForValue(startIndex);
  //       const endX = xAxis.getPixelForValue(endIndex);
  //       const topY = chart.chartArea.top;
  //       const bottomY = chart.chartArea.bottom;

  //       ctx.save();
  //       ctx.fillStyle = "rgba(255, 165, 0, 0.2)"; // 薄いオレンジ
  //       ctx.fillRect(startX, topY, endX - startX, bottomY - topY);
  //       ctx.restore();
  //     });
  //   },
  // };

  return (
    <Chart
      xLabels={minuteLabels}
      datasets={[
        {
          type: "line",
          label: "dip",
          data: dipEuel,
          borderColor: "blue",
          tension: 0.4,
          pointRadius: 0,
        },
        {
          type: "line",
          label: "offdip",
          data: offdipEuel,
          borderColor: "red",
          tension: 0.4,
          pointRadius: 0,
        },
      ]}
      xAxisTitle="UT Time"
      yAxisTitle="nT"
      plugins={[backgroundPlugin]} // プラグインを渡す
    />
  );
};

export default EejChart;
