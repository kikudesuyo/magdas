export const xLabel = () => {
  const labels = [];
  for (let i = 0; i < 1440; i++) {
    const hours = Math.floor(i / 60)
      .toString()
      .padStart(2, "0");
    const minutes = (i % 60).toString().padStart(2, "0");
    labels.push(`${hours}:${minutes}`);
  }
  return labels;
};
