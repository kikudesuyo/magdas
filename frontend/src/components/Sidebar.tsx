import { useState } from "react";
import { Link } from "react-router-dom";
import { PATHS } from "@/utils/constant";

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  const linkClass =
    "block px-4 py-2 hover:bg-slate-200 rounded-md transition-colors duration-200 text-slate-700 font-medium";

  return (
    <>
      <button
        onClick={toggleSidebar}
        className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
        aria-label="Toggle sidebar"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>

      {/* Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 transition-opacity"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar Drawer */}
      <aside
        className={`fixed top-0 right-0 z-50 h-full w-64 bg-slate-50 border-l border-slate-200 transition-all duration-300 ease-in-out transform ${
          isOpen
            ? "translate-x-0 opacity-100 visible"
            : "translate-x-full opacity-0 invisible"
        }`}
      >
        <div className="flex justify-between items-center p-4 border-b border-slate-200">
          <span className="font-semibold text-lg text-slate-700">Menu</span>
          <button
            onClick={() => setIsOpen(false)}
            className="p-1 hover:bg-slate-200 rounded-md transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <nav className="flex flex-col gap-2 p-4">
          <Link
            to={PATHS.HOME}
            className={linkClass}
            onClick={() => setIsOpen(false)}
          >
            Home
          </Link>
          <Link
            to={PATHS.EE_INDEX}
            className={linkClass}
            onClick={() => setIsOpen(false)}
          >
            EE-index Plot
          </Link>
          <Link
            to={PATHS.EEJ}
            className={linkClass}
            onClick={() => setIsOpen(false)}
          >
            EUEL Plot
          </Link>
          <Link
            to={PATHS.DOWNLOAD}
            className={linkClass}
            onClick={() => setIsOpen(false)}
          >
            Download
          </Link>
        </nav>
      </aside>
    </>
  );
};

export default Sidebar;
