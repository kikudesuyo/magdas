export const xLabel = (days: number = 1) => {
  const labels = [];
  const totalMinutes = 1440 * days; // 1440 minutes per day
  
  for (let i = 0; i < totalMinutes; i++) {
    const dayNumber = Math.floor(i / 1440);
    const minuteOfDay = i % 1440;
    
    const hours = Math.floor(minuteOfDay / 60)
      .toString()
      .padStart(2, "0");
    const minutes = (minuteOfDay % 60).toString().padStart(2, "0");
    
    // For multi-day display, add day information to labels at the start of each day
    if (days > 1 && minuteOfDay === 0) {
      labels.push(`Day ${dayNumber + 1} - 00:00`);
    } else if (days > 1 && minuteOfDay % 180 === 0) {
      // Add hour markers every 3 hours for multi-day view
      labels.push(`D${dayNumber + 1} ${hours}:${minutes}`);
    } else if (days === 1 || minuteOfDay % 60 === 0) {
      // For single day, show all hour:minute
      // For multi-day, only show hour markers
      labels.push(`${hours}:${minutes}`);
    } else {
      // For minutes that don't need special labels
      labels.push(`${hours}:${minutes}`);
    }
  }
  
  return labels;
};
