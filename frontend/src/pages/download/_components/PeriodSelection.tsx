import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { downloadFile } from "../helper/fileDownload";
import { STATIONS } from "@/utils/constant";
import { DateSelection, type DateValue } from "@/components";

interface FormData {
  stationCode: string;
  startDate: DateValue;
  endDate: DateValue;
}

// 日付を比較する関数
const compareDates = (date1: DateValue, date2: DateValue): number => {
  if (!date1.year || !date1.month || !date1.day || !date2.year || !date2.month || !date2.day) {
    return 0;
  }
  
  const d1 = new Date(
    parseInt(date1.year),
    parseInt(date1.month) - 1,
    parseInt(date1.day)
  );
  
  const d2 = new Date(
    parseInt(date2.year),
    parseInt(date2.month) - 1,
    parseInt(date2.day)
  );
  
  return d1.getTime() - d2.getTime();
};

const PeriodSelectionForm: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<FormData>({
    defaultValues: {
      stationCode: "ANC",
      startDate: { year: "2010", month: "05", day: "01" },
      endDate: { year: "2010", month: "05", day: "02" },
    },
  });

  const startDate = watch("startDate");
  const endDate = watch("endDate");

  // 開始日が変更されたときの処理
  useEffect(() => {
    if (startDate?.year && startDate?.month && startDate?.day && 
        endDate?.year && endDate?.month && endDate?.day) {
      // 開始日が終了日より未来の場合、終了日を開始日と同じにする
      if (compareDates(startDate, endDate) > 0) {
        setValue("endDate", { ...startDate });
      }
    }
  }, [startDate, endDate, setValue]);

  // 終了日が変更されたときの処理
  useEffect(() => {
    if (startDate?.year && startDate?.month && startDate?.day && 
        endDate?.year && endDate?.month && endDate?.day) {
      // 終了日が開始日より過去の場合、開始日を終了日と同じにする
      if (compareDates(startDate, endDate) > 0) {
        setValue("startDate", { ...endDate });
      }
    }
  }, [endDate, startDate, setValue]);

  const onSubmit = async (data: FormData) => {
    const props = {
      stationCode: data.stationCode,
      startDate: `${data.startDate.year}-${data.startDate.month}-${data.startDate.day}`,
      endDate: `${data.endDate.year}-${data.endDate.month}-${data.endDate.day}`,
    };
    await downloadFile(props);
  };

  // データ取得可能な期間を定義
  const availableDateRange = {
    startYear: 2000, // 2000年から
    endYear: 2023, // 2023年まで
  };

  return (
    <div className="flex flex-col p-4 w-4/5">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className=" bg-white p-6 rounded-lg shadow-md border border-gray-300 flex flex-col gap-4"
      >
        <h2 className="text-2xl font-semibold text-gray-700 text-center mb-6">
          ダウンロード
        </h2>

        <div>
          <label className="block text-gray-700 mb-2 font-bold">観測点</label>
          <div>
            <select
              {...register("stationCode")}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              {STATIONS.map((stationCode) => (
                <option key={stationCode} value={stationCode}>
                  {stationCode}
                </option>
              ))}
            </select>
          </div>
        </div>

        <DateSelection
          label="開始日"
          dateValue={watch("startDate") || { year: "", month: "", day: "" }}
          onChange={(date: DateValue) => {
            setValue("startDate", date);
          }}
          hasError={!!errors.startDate}
          errorMessage="開始日を正しく選択してください。"
          dateRange={availableDateRange}
        />

        <DateSelection
          label="終了日"
          dateValue={watch("endDate") || { year: "", month: "", day: "" }}
          onChange={(date: DateValue) => {
            setValue("endDate", date);
          }}
          hasError={!!errors.endDate}
          errorMessage="終了日を正しく選択してください。"
          dateRange={availableDateRange}
        />
        <button
          type="submit"
          className="w-full py-4 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 items-center"
        >
          確認
        </button>
      </form>
    </div>
  );
};

export default PeriodSelectionForm;
