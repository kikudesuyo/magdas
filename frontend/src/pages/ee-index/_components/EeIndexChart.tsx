import Chart from "@/components/chart/Chart";
import { xLabel } from "@/pages/ee-index/helper/xLabel";

type IndexProps = {
  values: {
    er: number[];
    edst: number[];
    euel: number[];
  };
  dates: string[];
};

const EeIndexChart = ({ values, dates }: IndexProps) => {
  const { er, edst, euel } = values;

  return (
    <Chart
      xLabels={xLabel(dates)}
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
