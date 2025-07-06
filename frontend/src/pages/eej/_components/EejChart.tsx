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
import { useMemo } from "react";

ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  LineController,
  Tooltip,
  Legend
);

type IndexProps = {
  values: {
    dipEuel: number[];
    offdipEuel: number[];
  };
  minuteLabels: string[];
  singularEejDates: string[];
};

const createBackgroundPlugin = (
  singularEejDates: string[]
): Plugin<"line"> => ({
  id: "eejBackgroundPlugin",
  afterDatasetsDraw: (chart) => {
    const ctx = chart.ctx;
    const xAxis = chart.scales.x;
    const yAxis = chart.scales.y;

    console.log("🎨 Background plugin executing...");
    console.log("📅 singularEejDates:", singularEejDates);

    ctx.save();

    if (!singularEejDates?.length) {
      console.log("❌ No dates to highlight");
      ctx.restore();
      return;
    }

    const chartLabels = chart.data.labels as string[];
    console.log("📊 Chart labels length:", chartLabels.length);

    // 📈 全ての日付のインデックスを計算
    const dateRanges = singularEejDates
      .map((dateStr) => {
        const startIndex = chartLabels.findIndex((label) =>
          label.startsWith(dateStr)
        );
        let endIndex = -1;
        for (let i = chartLabels.length - 1; i >= startIndex; i--) {
          if (chartLabels[i].startsWith(dateStr)) {
            endIndex = i;
            break;
          }
        }

        console.log(`📍 ${dateStr}: start=${startIndex}, end=${endIndex}`);
        return { dateStr, startIndex, endIndex };
      })
      .filter((range) => range.startIndex !== -1 && range.endIndex !== -1);

    console.log("✅ Valid date ranges:", dateRanges.length);

    if (dateRanges.length === 0) {
      console.log("❌ No valid date ranges found");
      ctx.restore();
      return;
    }

    ctx.fillStyle = "rgba(255, 165, 0, 0.3)";

    dateRanges.forEach(({ dateStr, startIndex, endIndex }) => {
      const startX = xAxis.getPixelForValue(startIndex);
      const endX = xAxis.getPixelForValue(endIndex);
      const width = Math.max(endX - startX, 1);

      console.log(`🎨 Drawing ${dateStr}: x=${startX}, width=${width}`);
      ctx.fillRect(startX, yAxis.top, width, yAxis.height);
    });

    ctx.restore();
    console.log("✅ Background plugin completed");
  },
});

const EejChart = ({ values, minuteLabels, singularEejDates }: IndexProps) => {
  const { dipEuel, offdipEuel } = values;

  console.log("🚀 EejChart rendering...");
  console.log("📊 Data lengths:", {
    dipEuel: dipEuel.length,
    offdipEuel: offdipEuel.length,
    minuteLabels: minuteLabels.length,
    singularEejDates: singularEejDates.length,
  });

  // 🚀 データのメモ化
  const chartData = useMemo(() => {
    console.log("📈 Creating chart data...");
    return {
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
  }, [dipEuel, offdipEuel, minuteLabels]);

  const chartOptions: ChartOptions<"line"> = useMemo(
    () => ({
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: "index" as const,
      },
      scales: {
        x: {
          type: "category",
          ticks: {
            autoSkip: true,
            maxRotation: 45,
          },
        },
        y: {
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
    }),
    []
  );

  // 🎯 プラグインのメモ化 - キーとなる修正点
  const backgroundPlugin = useMemo(() => {
    console.log("🔧 Creating background plugin with dates:", singularEejDates);
    return createBackgroundPlugin(singularEejDates);
  }, [singularEejDates]);

  // 🔍 最終的なレンダリング前のチェック
  console.log("🎯 Final render check:", {
    hasData: chartData.labels.length > 0,
    hasDates: singularEejDates.length > 0,
    pluginReady: !!backgroundPlugin,
  });

  return (
    <div className="w-[800px] h-[400px]">
      <ReactChartJS
        type="line"
        data={chartData}
        options={chartOptions}
        plugins={[backgroundPlugin]}
      />
    </div>
  );
};

export default EejChart;
