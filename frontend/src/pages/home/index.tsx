import Main from "@/components/Main";
import { Link } from "react-router-dom";
import { PATHS } from "@/utils/constant";
import References from "@/pages/home/_components/References";
import MagdasMap from "@/assets/imgs/magdas_map.png";

const Home = () => {
  return (
    <Main style="items-center gap-12 pt-4">
      <div className="flex flex-col gap-12 items-center justify-center">
        <div className="flex flex-row gap-12 items-center justify-center">
          <Link
            to={PATHS.EE_INDEX}
            className="text-3xl bg-slate-200 px-4 py-3 hover:bg-slate-400 rounded-lg border border-slate-400"
          >
            EE-index Plot
          </Link>
          <Link
            to={PATHS.EEJ}
            className="text-3xl bg-slate-200 px-4 py-3 hover:bg-slate-400 rounded-lg border border-slate-400"
          >
            Peculiar EEJ Detection
          </Link>
          <Link
            to={PATHS.DOWNLOAD}
            className="text-3xl bg-slate-200 px-4 py-3 hover:bg-slate-400 rounded-lg border border-slate-400"
          >
            Download
          </Link>
        </div>
        <img src={MagdasMap} alt="" className="max-w-4xl" />
        <References />
      </div>
    </Main>
  );
};
export default Home;
