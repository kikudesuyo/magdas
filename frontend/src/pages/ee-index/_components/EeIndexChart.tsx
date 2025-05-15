import Chart from "@/components/chart/Chart";

type IndexProps = {
  values: {
    er: number[];
    edst: number[];
    euel: number[];
  };
  minuteLabels: string[];
};

const EeIndexChart = ({ values, minuteLabels }: IndexProps) => {
  const { er, edst, euel } = values;

  return (
    <Chart
      xLabels={minuteLabels}
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
