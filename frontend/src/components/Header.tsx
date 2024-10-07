import { Link } from "react-router-dom";
import iSpesLogo from "@/assets/imgs/i-spes-logo.png";

const Header = () => {
  return (
    <header className="sticky top-0 flex justify-between border-b border-slate-300 bg-white p-3">
      <Link to="/" className="flex flex-col justify-center text-xl">
        <img src={iSpesLogo} />
      </Link>
      <div className="flex gap-2"></div>
    </header>
  );
};

export default Header;
