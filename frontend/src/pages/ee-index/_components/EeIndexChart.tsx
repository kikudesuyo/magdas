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
  
  // Generate labels for multiple days
  const labels = xLabel(dates.length);
  
  // Add date information to the chart title
  const dateRange = dates.length > 0 
    ? dates.length === 1 
      ? dates[0] 
      : `${dates[0]} ~ ${dates[dates.length - 1]}`
    : "";
  
  return (
    <div className="flex flex-col items-center">
      {dateRange && <h2 className="text-lg font-semibold mb-2">{dateRange}</h2>}
      <Chart
        xLabels={labels}
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
    </div>
  );
};
export default EeIndexChart;
