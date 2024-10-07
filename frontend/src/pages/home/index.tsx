import Main from "@/components/Main";
import { Link } from "react-router-dom";
import { PATHS } from "@/utils/constant";

const Home = () => {
  return (
    <Main style="items-center gap-8 pt-4">
      <div className="flex flex-row gap-12">
        <Link
          to={PATHS.EE_INDEX}
          className="text-2xl bg-slate-200 px-4 py-3 hover:bg-slate-400 round-xl"
        >
          EE-indexのプロットページ
        </Link>
        <Link
          to={PATHS.DOWNLOAD}
          className="text-2xl bg-slate-200 px-4 py-3 hover:bg-slate-400 rounded-lg"
        >
          ダウンロードページ
        </Link>
      </div>
    </Main>
  );
};
export default Home;
