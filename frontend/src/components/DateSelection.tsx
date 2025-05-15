import React from "react";

interface DateSelectionProps {
  label: string;
  yearValue: string;
  monthValue: string;
  dayValue: string;
  onYearChange: (value: string) => void;
  onMonthChange: (value: string) => void;
  onDayChange: (value: string) => void;
  hasError?: boolean;
  errorMessage?: string;
}

const DateSelection: React.FC<DateSelectionProps> = ({
  label,
  yearValue,
  monthValue,
  dayValue,
  onYearChange,
  onMonthChange,
  onDayChange,
  hasError = false,
  errorMessage = "日付を正しく選択してください。",
}) => {
  const years = Array.from({ length: 50 }, (_, i) => String(1970 + i)); // 1970年から50年分
  const months = Array.from({ length: 12 }, (_, i) =>
    String(i + 1).padStart(2, "0")
  ); // 1~12月
  const days = Array.from({ length: 31 }, (_, i) =>
    String(i + 1).padStart(2, "0")
  ); // 1~31日

  return (
    <div className="mb-4">
      <label className="block text-gray-700 mb-2 font-bold">{label}</label>
      <div className="flex space-x-2">
        <select
          value={yearValue}
          onChange={(e) => onYearChange(e.target.value)}
          className="w-1/3 px-3 py-2 border border-gray-300 rounded-md focus:outline-none"
        >
          <option value="">年</option>
          {years.map((year) => (
            <option key={year} value={year}>
              {year}
            </option>
          ))}
        </select>
        <select
          value={monthValue}
          onChange={(e) => onMonthChange(e.target.value)}
          className="w-1/3 px-3 py-2 border border-gray-300 rounded-md focus:outline-none"
        >
          <option value="">月</option>
          {months.map((month) => (
            <option key={month} value={month}>
              {month}
            </option>
          ))}
        </select>
        <select
          value={dayValue}
          onChange={(e) => onDayChange(e.target.value)}
          className="w-1/3 px-3 py-2 border border-gray-300 rounded-md focus:outline-none"
        >
          <option value="">日</option>
          {days.map((day) => (
            <option key={day} value={day}>
              {day}
            </option>
          ))}
        </select>
      </div>
      {hasError && <p className="text-red-600 text-sm mt-1">{errorMessage}</p>}
    </div>
  );
};

export default DateSelection;