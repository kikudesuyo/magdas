import Chart from "@/components/chart/Chart";
import { xLabel } from "@/features/chart/xLabel";

type IndexProps = {
  values: {
    er: number[];
    edst: number[];
    euel: number[];
  };
  date: string;
};

const EeIndexChart = ({ values, date }: IndexProps) => {
  const { er, edst, euel } = values;
  console.log(date);
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
