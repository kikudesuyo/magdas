import Chart from "@/components/chart/Chart";
import { xLabel } from "@/components/chart/xLabel";

type IndexProps = {
  values: {
    er: number[];
    edst: number[];
    euel: number[];
  };
  date: string;
};

const EeIndexChart = ({ values, date }: IndexProps) => {
  console.log(date);
  const er = values.er;
  const edst = values.edst;
  const euel = values.euel;
  return (
    <Chart
      xLabels={xLabel()}
      datasets={[
        {
          type: "line",
          label: "EDst",
          data: edst,
          borderColor: "blue",
          tension: 0.4,
          pointRadius: 0,
        },
        {
          type: "line",
          label: "ER",
          data: er,
          borderColor: "red",
          tension: 0.4,
          pointRadius: 0,
        },
        {
          type: "line",
          label: "EUEL",
          data: euel,
          borderColor: "green",
          tension: 0.4,
          pointRadius: 0,
        },
      ]}
      xAxisTitle="UT Time"
      yAxisTitle="nT"
    />
  );
};
export default EeIndexChart;
