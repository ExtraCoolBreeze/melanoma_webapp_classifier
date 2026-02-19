import { Link } from "react-router-dom";

function SiteHeader() {
  return (
    <header className="bg-[#EDEEEE] text-[#005EB8] py-4 shadow-md" id="top">
      <div className="max-w-full mx-auto px-4 flex items-center justify-between gap-10">
        <div className="flex items-center gap-4">
          <img src="/LogoIcon.svg" alt="Spot Check Medical Logo" className="w-25 h-25" />
          <div className="text-6xl font-semibold whitespace-nowrap">Spot Check Medical</div>
        </div>

        <Link to="/" className="text-black hover:text-[#005EB8] pr-20 font-medium transition-colors underline">
          Home
        </Link>
      </div>
    </header>
  );
}

export default SiteHeader;