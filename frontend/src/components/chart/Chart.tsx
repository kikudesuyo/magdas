import {
  Chart as ChartJS,
  ChartData,
  ChartOptions,
  LineController,
  LineElement,
  LinearScale,
  CategoryScale,
  BarController,
  BarElement,
  PointElement,
  Legend,
  RadialLinearScale,
  Tooltip,
} from "chart.js";
import { Chart as ReactChartJS } from "react-chartjs-2";

type ChartType = "line";

export type ChartDataset = {
  type: ChartType;
  label: string;
  data: number[];
  borderColor?: string;
  backgroundColor?: string;
  borderDash?: number[];
  tension: number;
  pointRadius: number;
};

export type Props = {
  xLabels: string[];
  datasets: ChartDataset[];
  xAxisTitle: string;
  yAxisTitle: string;
};

const Chart = ({ xLabels, datasets, xAxisTitle, yAxisTitle }: Props) => {
  ChartJS.register(
    LineController,
    LineElement,
    LinearScale,
    CategoryScale,
    BarController,
    BarElement,
    PointElement,
    RadialLinearScale,
    Legend,
    Tooltip
  );

  const data: ChartData = {
    datasets: datasets,
    labels: xLabels,
  };

  const options: ChartOptions = {
    scales: {
      x: {
        title: {
          display: true,
          text: xAxisTitle,
        },
      },
      y: {
        title: {
          display: true,
          text: yAxisTitle,
        },
      },
    },
    plugins: {
      legend: {
        position: "bottom",
      },
    },
    responsive: true,
  };

  return (
    <div className="w-full max-w-lg">
      <ReactChartJS type={"line"} data={data} options={options} width={300} />
    </div>
  );
};

export default Chart;
