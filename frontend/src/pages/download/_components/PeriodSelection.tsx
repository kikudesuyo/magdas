import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { downloadFile } from "../helper/fileDownload";
import { STATIONS } from "@/utils/constant";
import { DateSelection, DateValue } from "@/components";

interface FormData {
  stationCode: string;
  startDate: DateValue;
  endDate: DateValue;
}

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

  useEffect(() => {
    if (startDate?.year && startDate?.month && startDate?.day) {
      setValue("endDate", { ...startDate });
    }
  }, [startDate, setValue]);

  const onSubmit = async (data: FormData) => {
    const props = {
      stationCode: data.stationCode,
      startDate: `${data.startDate.year}-${data.startDate.month}-${data.startDate.day}`,
      endDate: `${data.endDate.year}-${data.endDate.month}-${data.endDate.day}`,
    };
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
          value={watch("startDate") || { year: "", month: "", day: "" }}
          onChange={(date: DateValue) => {
            setValue("startDate", date);
          }}
          hasError={!!errors.startDate}
          errorMessage="開始日を正しく選択してください。"
        />

        <DateSelection
          label="終了日"
          value={watch("endDate") || { year: "", month: "", day: "" }}
          onChange={(date: DateValue) => {
            setValue("endDate", date);
          }}
          hasError={!!errors.endDate}
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
