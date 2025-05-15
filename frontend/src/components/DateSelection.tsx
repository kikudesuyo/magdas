import React, { useMemo } from "react";
import { getDaysInMonth, isValid } from "date-fns";

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
  dateValue: DateValue;
  dateRange: DateRange;
  onChange: (date: DateValue) => void;
  hasError?: boolean;
  errorMessage?: string;
}

const adjustDayIfInvalid = (date: DateValue): DateValue => {
  const year = parseInt(date.year);
  const month = parseInt(date.month) - 1; // date-fnsは0-11の月を使用
  const day = parseInt(date.day);

  const dateObj = new Date(year, month, day);

  if (!isValid(dateObj) || dateObj.getDate() !== day) {
    // 無効な日付(e.g. 2023-02-30)の場合、その月の最大日数に調整
    const maxDay = getDaysInMonth(new Date(year, month));
    return { ...date, day: String(Math.min(day, maxDay)).padStart(2, "0") };
  }

  return date;
};

const DateSelection: React.FC<DateSelectionProps> = ({
  label,
  dateValue,
  dateRange,
  onChange,
  hasError = false,
  errorMessage = "",
}) => {
  const { startYear, endYear } = dateRange;
  const years = Array.from({ length: endYear - startYear + 1 }, (_, i) =>
    String(startYear + i)
  );

  const months = Array.from({ length: 12 }, (_, i) =>
    String(i + 1).padStart(2, "0")
  );

  const days = useMemo(() => {
    if (!dateValue.year || !dateValue.month) {
      return Array.from({ length: 31 }, (_, i) =>
        String(i + 1).padStart(2, "0")
      );
    }

    const year = parseInt(dateValue.year);
    const month = parseInt(dateValue.month) - 1; // date-fnsは0-11の月を使用

    return Array.from(
      { length: getDaysInMonth(new Date(year, month)) },
      (_, i) => String(i + 1).padStart(2, "0")
    );
  }, [dateValue.year, dateValue.month]);

  const { year, month, day } = dateValue;

  const handleChange = (updated: Partial<DateValue>) => {
    let newValue: DateValue = {
      year: updated.year ?? year,
      month: updated.month ?? month,
      day: updated.day ?? day,
    };

    if ((updated.year || updated.month) && newValue.day) {
      newValue = adjustDayIfInvalid(newValue);
    }

    onChange(newValue);
  };

  return (
    <div className="mb-4">
      <label className="block text-gray-700 mb-2 font-bold">{label}</label>
      <div className="flex space-x-2">
        <select
          value={dateValue.year}
          onChange={(e) => handleChange({ year: e.target.value })}
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
          value={dateValue.month}
          onChange={(e) => handleChange({ month: e.target.value })}
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
          value={dateValue.day}
          onChange={(e) => handleChange({ day: e.target.value })}
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
