import { Link, useNavigate } from "react-router-dom";
import Button from "@/components/Button";
import { PATHS } from "@/utils/constant";

const Header = () => {
  const navigate = useNavigate();
  return (
    <header className="sticky top-0 flex justify-between border-b border-black bg-white p-3">
      <Link to="/" className="flex flex-col justify-center text-xl">
        トップページ
      </Link>
      <div className="flex gap-2">
        <Button
          label="プロットページへ"
          func={() => {
            navigate(PATHS.PLOT);
          }}
        />
      </div>
    </header>
  );
};

export default Header;
