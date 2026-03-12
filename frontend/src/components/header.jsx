import { Link } from "react-router-dom";

function SiteHeader() {
  return (
    <header className="bg-[#EDEEEE] text-[#005EB8] py-4 shadow-md" id="top">
      <div className="max-w-full mx-auto px-4 flex items-center justify-between gap-20">
        <div className="flex items-center gap-4">
          <img src="/LogoIcon.svg" alt="Spot Check Medical Logo" className="w-12 h-12 md:w-16 md:h-16 lg:w-25 lg:h-25" />
          <div className="text-2xl md:text-4xl lg:text-6xl font-semibold whitespace-nowrap">Spot Check Medical</div>
        </div>

        <Link to="/" className="text-black hover:text-[#005EB8] pr-20 font-medium transition-colors underline shrink-0">
          Home
        </Link>
      </div>
    </header>
  );
}

export default SiteHeader;