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
