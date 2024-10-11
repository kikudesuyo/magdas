import PeriodSelectionForm from "@/pages/download/_components/PeriodSelection";
import Description from "@/pages/download/_components/Description";
import Main from "@/components/Main";

const Download = () => {
  return (
    <Main style="items-center gap-10">
      <h1 className="text-4xl font-bold text-slate-600 mt-8">
        EE-index Download
      </h1>
      <Description />
      <PeriodSelectionForm />
    </Main>
  );
};

export default Download;
