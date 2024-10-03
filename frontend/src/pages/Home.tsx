import Main from "@/components/Main";
import DownloadButton from "@/features/download/Download";

const Home = () => {
  return (
    <Main style="items-center gap-8 pt-4">
      <h1 className="text-3xl">MAGDAS EE-indexのプロット</h1>
      <DownloadButton />
    </Main>
  );
};
export default Home;
