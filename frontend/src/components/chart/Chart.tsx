import {
  Chart as ChartJS,
  ChartData,
  ChartOptions,
  Plugin,
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
  plugins?: Plugin[]; // 追加
};

const Chart = ({
  xLabels,
  datasets,
  xAxisTitle,
  yAxisTitle,
  plugins,
}: Props) => {
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
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: "index",
      intersect: false,
    },
    scales: {
      x: {
        title: {
          display: true,
          text: xAxisTitle,
        },
        ticks: {
          maxTicksLimit: 6,
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
  };

  return (
    <div className="w-full max-w-7xl">
      <ReactChartJS
        type={"line"}
        data={data}
        options={options}
        plugins={plugins}
      />
    </div>
  );
};

export default Chart;
