import React from "react";
import { useForm } from "react-hook-form";
import { downloadFile } from "../helper/fileDownload";

interface FormData {
  startYear: string;
  startMonth: string;
  startDay: string;
  endYear: string;
  endMonth: string;
  endDay: string;
}

const PeriodSelectionForm: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>();

  const years = Array.from({ length: 50 }, (_, i) => String(1970 + i)); // 1970年から50年分
  const months = Array.from({ length: 12 }, (_, i) =>
    String(i + 1).padStart(2, "0")
  ); // 1~12月
  const days = Array.from({ length: 31 }, (_, i) =>
    String(i + 1).padStart(2, "0")
  ); // 1~31日

  const onSubmit = async (data: FormData) => {
    data;
    // const startDate = `${data.startYear}-${data.startMonth}-${data.startDay}`;
    // const endDate = `${data.endYear}-${data.endMonth}-${data.endDay}`;
    // const station = "ANC";
    // fetchCustomDateFile({ startDate, endDate, station });
    const props = {
      startDate: "2014-06-10",
      endDate: "2014-06-11",
      station: "ANC",
    };
    await downloadFile(props);
  };

  return (
    <div className="flex flex-col p-4 w-4/5">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className=" bg-white p-6 rounded-lg shadow-md border border-gray-300 "
      >
        <h2 className="text-2xl font-semibold text-gray-700 text-center mb-6">
          ダウンロード期間
        </h2>

        <div className="mb-4">
          <label className="block text-gray-700  mb-2 font-bold">開始日</label>
          <div className="flex space-x-2">
            <select
              {...register("startYear", { required: "開始年は必須です" })}
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
              {...register("startMonth", { required: "開始月は必須です" })}
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
              {...register("startDay", { required: "開始日は必須です" })}
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
          {(errors.startYear || errors.startMonth || errors.startDay) && (
            <p className="text-red-600 text-sm mt-1">
              開始日を正しく選択してください。
            </p>
          )}
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">終了日</label>
          <div className="flex space-x-2">
            <select
              {...register("endYear", { required: "終了年は必須です" })}
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
              {...register("endMonth", { required: "終了月は必須です" })}
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
              {...register("endDay", { required: "終了日は必須です" })}
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
          {(errors.endYear || errors.endMonth || errors.endDay) && (
            <p className="text-red-600 text-sm mt-1">
              終了日を正しく選択してください。
            </p>
          )}
        </div>

        <button
          type="submit"
          className="w-full py-2 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700"
        >
          確認
        </button>
      </form>
    </div>
  );
};

export default PeriodSelectionForm;
