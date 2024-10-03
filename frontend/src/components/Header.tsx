import { Link, useNavigate } from "react-router-dom";
import Button from "@/components/button/Button";
import { PATHS } from "@/utils/constant";
import iSpesLogo from "@/assets/imgs/i-spes-logo.png";

const Header = () => {
  const navigate = useNavigate();
  return (
    <header className="sticky top-0 flex justify-between border-b border-black bg-white p-3">
      <Link to="/" className="flex flex-col justify-center text-xl">
        <img src={iSpesLogo} />
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
