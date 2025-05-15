import React, { useMemo } from "react";
import { getDaysInMonth, isValid, setDate } from "date-fns";

export interface DateValue {
  year: string;
  month: string;
  day: string;
}

export interface DateRange {
  startYear: number;
  endYear: number;
}

interface DateSelectionProps {
  label: string;
  value: DateValue;
  onChange: (date: DateValue) => void;
  hasError?: boolean;
  errorMessage?: string;
  dateRange?: DateRange;
}

const DateSelection: React.FC<DateSelectionProps> = ({
  label,
  value,
  onChange,
  hasError = false,
  errorMessage = "",
  dateRange = { startYear: 1970, endYear: 2020 }, // デフォルトの範囲
}) => {
  // 年の範囲を生成
  const years = useMemo(() => {
    const { startYear, endYear } = dateRange;
    const length = endYear - startYear + 1;
    return Array.from({ length }, (_, i) => String(startYear + i));
  }, [dateRange]);

  // 月の配列を生成
  const months = useMemo(() => {
    return Array.from({ length: 12 }, (_, i) =>
      String(i + 1).padStart(2, "0")
    ); // 1~12月
  }, []);

  // 選択された年と月に基づいて日の配列を生成
  const days = useMemo(() => {
    if (!value.year || !value.month) {
      return Array.from({ length: 31 }, (_, i) => String(i + 1).padStart(2, "0"));
    }

    const year = parseInt(value.year);
    const month = parseInt(value.month) - 1; // date-fnsは0-11の月を使用
    
    // date-fnsを使用して月の日数を取得
    const daysInMonth = getDaysInMonth(new Date(year, month));
    
    return Array.from({ length: daysInMonth }, (_, i) =>
      String(i + 1).padStart(2, "0")
    );
  }, [value.year, value.month]);

  const handleYearChange = (year: string) => {
    // 年が変わった場合、日付が月の最大日数を超えていないか確認
    const newValue = { ...value, year };
    
    if (newValue.month && newValue.day) {
      const monthNum = parseInt(newValue.month) - 1; // date-fnsは0-11の月を使用
      const day = parseInt(newValue.day);
      const yearNum = parseInt(year);
      
      // date-fnsを使用して日付が有効かチェック
      const dateObj = new Date(yearNum, monthNum, day);
      
      if (!isValid(dateObj) || dateObj.getDate() !== day) {
        // 無効な日付の場合、その月の最大日数に調整
        const daysInMonth = getDaysInMonth(new Date(yearNum, monthNum));
        newValue.day = String(Math.min(day, daysInMonth)).padStart(2, "0");
      }
    }
    
    onChange(newValue);
  };

  const handleMonthChange = (month: string) => {
    // 月が変わった場合、日付が月の最大日数を超えていないか確認
    const newValue = { ...value, month };
    
    if (newValue.year && newValue.day) {
      const monthNum = parseInt(month) - 1; // date-fnsは0-11の月を使用
      const day = parseInt(newValue.day);
      const yearNum = parseInt(newValue.year);
      
      // date-fnsを使用して日付が有効かチェック
      const dateObj = new Date(yearNum, monthNum, day);
      
      if (!isValid(dateObj) || dateObj.getDate() !== day) {
        // 無効な日付の場合、その月の最大日数に調整
        const daysInMonth = getDaysInMonth(new Date(yearNum, monthNum));
        newValue.day = String(Math.min(day, daysInMonth)).padStart(2, "0");
      }
    }
    
    onChange(newValue);
  };

  const handleDayChange = (day: string) => {
    onChange({ ...value, day });
  };

  return (
    <div className="mb-4">
      <label className="block text-gray-700 mb-2 font-bold">{label}</label>
      <div className="flex space-x-2">
        <select
          value={value.year}
          onChange={(e) => handleYearChange(e.target.value)}
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
          value={value.month}
          onChange={(e) => handleMonthChange(e.target.value)}
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
          value={value.day}
          onChange={(e) => handleDayChange(e.target.value)}
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
