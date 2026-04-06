//Name: Craig McMillan
//Student Number: S2390641
//Date: 14/03/26
//The footer is a reusable component that is used across all pages, includes naigation links 

function SiteFooter() {
  return (
<footer className="bg-white text-black py-8 mt-auto">
  <div className="max-w-300 mx-auto px-8">
    <div className="grid grid-cols-[1fr_2fr_1fr] gap-2 mb-4">
      <div text-right>
        <button type="button" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })} className=" text-black hover:text-[#005EB8] transition-colors cursor-pointer underline bg-transparent border-none p-0"> Back to Top</button>
      </div>
      <div></div>
      <div className="text-right">
        <a className="text-black hover:text-[#005EB8] transition-colors underline whitespace-nowrap" href="https://www.nhs.uk/conditions/melanoma-skin-cancer/" target="_blank">
          NHS Skin Cancer Website
        </a>
      </div>
    </div>
    <div className="text-center">
      @ Copyright Spot Check Medical 2026
    </div>
  </div>
</footer>
  );
}

export default SiteFooter;