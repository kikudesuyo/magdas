export const xLabel = (dates: string[]) => {
  const labels: string[] = [];

  for (const date of dates) {
    const baseDate = new Date(date); // 各日付の 00:00 を起点にする

    for (let i = 0; i < 1440; i++) {
      const labelDate = new Date(baseDate);
      labelDate.setMinutes(labelDate.getMinutes() + i);

      const year = labelDate.getFullYear();
      const month = (labelDate.getMonth() + 1).toString().padStart(2, "0");
      const day = labelDate.getDate().toString().padStart(2, "0");
      const hours = labelDate.getHours().toString().padStart(2, "0");
      const minutes = labelDate.getMinutes().toString().padStart(2, "0");

      labels.push(`${year}-${month}-${day} ${hours}:${minutes}`);
    }
  }

  return labels;
};
