import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  LineController,
  Tooltip,
  Legend,
  Plugin,
  ChartOptions,
} from "chart.js";
import { Chart as ReactChartJS } from "react-chartjs-2";
import { EejPlotData } from "@/pages/eej";

ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  LineController,
  Tooltip,
  Legend
);

const EejChart = (eejPlotData: EejPlotData) => {
  const {
    values,
    minuteLabels,
    peculiarEejDates: peculiarEejDates,
  } = eejPlotData;
  const dipEuel = values.dipEuel;
  const offdipEuel = values.offdipEuel;

  const chartData = {
    labels: minuteLabels,
    datasets: [
      {
        label: "dipEuel",
        data: dipEuel,
        borderColor: "rgb(59, 130, 246)",
        borderWidth: 1,
        fill: false,
        pointRadius: 0,
        tension: 0,
      },
      {
        label: "offdipEuel",
        data: offdipEuel,
        borderColor: "rgb(239, 68, 68)",
        borderWidth: 1,
        fill: false,
        pointRadius: 0,
        tension: 0,
      },
    ],
  };

  const chartOptions: ChartOptions<"line"> = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
      mode: "index" as const,
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Local Time",
          font: {
            size: 20,
          },
        },
        type: "category",
        ticks: {
          autoSkip: true,
          maxTicksLimit: 6,
        },
      },
      y: {
        min: -100,
        max: 200,
        beginAtZero: true,
      },
    },
    plugins: {
      legend: {
        display: true,
        position: "top" as const,
      },
    },
    animation: {
      duration: 0,
    },
    elements: {
      point: {
        radius: 0,
      },
    },
  };

  const backgroundPlugin: Plugin<"line"> = {
    id: "eejBackgroundPlugin",
    afterDatasetsDraw: (chart) => {
      if (!peculiarEejDates?.length) return;

      const ctx = chart.ctx;
      const xAxis = chart.scales.x;
      const yAxis = chart.scales.y;
      const chartLabels = chart.data.labels as string[];

      ctx.save();
      ctx.fillStyle = "rgba(255, 165, 0, 0.3)";

      peculiarEejDates.forEach((dateStr) => {
        const indices = chartLabels.reduce((acc, label, index) => {
          if (label.startsWith(dateStr)) {
            acc.push(index);
          }
          return acc;
        }, [] as number[]);

        if (indices.length > 0) {
          const startX = xAxis.getPixelForValue(indices[0]);
          const endX = xAxis.getPixelForValue(indices[indices.length - 1]);
          const width = Math.max(endX - startX, 1);
          ctx.fillRect(startX, yAxis.top, width, yAxis.height);
        }
      });

      ctx.restore();
    },
  };

  return (
    <div className="w-[800px] h-[400px]">
      <ReactChartJS
        key={peculiarEejDates.join(",")}
        type="line"
        data={chartData}
        options={chartOptions}
        plugins={[backgroundPlugin]}
      />
    </div>
  );
};

export default EejChart;
