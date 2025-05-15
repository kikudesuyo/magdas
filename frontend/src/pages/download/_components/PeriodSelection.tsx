import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { downloadFile } from "../helper/fileDownload";
import { STATIONS } from "@/utils/constant";
import { DateSelection } from "@/components";

interface FormData {
  startYear: string;
  startMonth: string;
  startDay: string;
  endYear: string;
  endMonth: string;
  endDay: string;
}

const PeriodSelectionForm: React.FC = () => {
  const [stationCode, setStationCode] = React.useState("ANC");
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<FormData>();

  const startYear = watch("startYear");
  const startMonth = watch("startMonth");
  const startDay = watch("startDay");

  const requiredField = (label: string) => ({
    required: `${label}は必須です`,
  });

  useEffect(() => {
    if (startYear && startMonth && startDay) {
      setValue("endYear", startYear);
      setValue("endMonth", startMonth);
      setValue("endDay", startDay);
    }
  }, [startYear, startMonth, startDay, setValue]);

  // 日付選択はDateSelectionコンポーネントに移動

  const onSubmit = async (data: FormData) => {
    const startDate = `${data.startYear}-${data.startMonth}-${data.startDay}`;
    const endDate = `${data.endYear}-${data.endMonth}-${data.endDay}`;
    const props = { startDate, endDate, stationCode };
    await downloadFile(props);
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
              value={stationCode}
              onChange={(e) => setStationCode(e.target.value)}
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
          yearValue={watch("startYear") || ""}
          monthValue={watch("startMonth") || ""}
          dayValue={watch("startDay") || ""}
          onYearChange={(value) => setValue("startYear", value)}
          onMonthChange={(value) => setValue("startMonth", value)}
          onDayChange={(value) => setValue("startDay", value)}
          hasError={!!(errors.startYear || errors.startMonth || errors.startDay)}
          errorMessage="開始日を正しく選択してください。"
        />

        <DateSelection
          label="終了日"
          yearValue={watch("endYear") || ""}
          monthValue={watch("endMonth") || ""}
          dayValue={watch("endDay") || ""}
          onYearChange={(value) => setValue("endYear", value)}
          onMonthChange={(value) => setValue("endMonth", value)}
          onDayChange={(value) => setValue("endDay", value)}
          hasError={!!(errors.endYear || errors.endMonth || errors.endDay)}
          errorMessage="終了日を正しく選択してください。"
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
