import { useLocation, useNavigate } from "react-router-dom";
import SiteHeader from "../components/header";
import SiteFooter from "../components/footer";

function AnalysisPage() {
  const location = useLocation();
  const navigate = useNavigate();

  let predictionData = null;
  let imageUrl = null;
  let fileName = null;

  if (location.state) {
    predictionData = location.state.predictionData;
    imageUrl = location.state.imageUrl;
    fileName = location.state.fileName;
  }

  let confidencePercent = null;
  if (predictionData) {
    confidencePercent = (predictionData.confidence * 100).toFixed(2);
  }

  let resultsContent;
  if (!predictionData) {
    resultsContent = (
      <div>
        <h1 className="text-5xl font-normal leading-tight mb-6">Analysis Results</h1>
        <p className="mb-4">No results to display</p>
        <div className="flex gap-4 justify-center mt-8">
          <button className="bg-[#005EB8] hover:opacity-90 text-white font-semibold px-8 py-3 rounded-lg transition-opacity underline" onClick={() => navigate("/")}>
            Go back
          </button>
        </div>
      </div>
    );
  } else {
    let imageDisplayElement = null;
    if (imageUrl) {
      let displayFileName = "Uploaded Image";
      if (fileName) {
        displayFileName = fileName.toUpperCase();
      }

      imageDisplayElement = (
        <div className="flex justify-center mb-8">
          <div>
            <div className="w-100 h-100 border-2 border-gray-300 rounded-xl flex items-center justify-center overflow-hidden bg-[#EDEEEE]">
              <img src={imageUrl} alt="Uploaded image" className="max-w-full max-h-full object-contain"/>
            </div>
            <div className="text-center mt-2 font-medium text-black text-sm">
              {displayFileName}
            </div>
          </div>
        </div>
      );
    }

    resultsContent = (
      <div>
        <h1 className="text-5xl font-normal leading-tight mb-6">Analysis Results</h1>

        {imageDisplayElement}
        <p className="mb-4">
          <strong>Prediction:</strong> {predictionData.label}
        </p>

        <p className="mb-4">
          <strong>Confidence:</strong> {confidencePercent}%
        </p>

        <h3 className="text-2xl font-semibold mb-4 mt-6">Class Probabilities</h3>

        <pre className="bg-black text-white p-4 rounded-lg overflow-x-auto font-mono text-sm leading-relaxed">
          {JSON.stringify(predictionData.probabilities, null, 2)}
        </pre>

        <div className="flex gap-4 justify-center mt-8">
          <button className="bg-[#005EB8] hover:opacity-90 text-white font-semibold px-8 py-3 rounded-lg transition-opacity underline" onClick={() => navigate("/")}>
            Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-[#005EB8]">
      <SiteHeader />
      <div className="w-full px-8 py-8 flex-1">
        <div className="bg-white p-8 rounded-xl my-8 text-black">
          <h2 className="text-2xl font-semibold mb-4 mt-0">About</h2>
          <p className="mb-4 leading-relaxed">
            Spot Check Medical is an academic prototype web application designed to assist with the analysis of skin lesion images as part of an undergraduate honours project.
            This application explores the use of deep learning techniques for medical image classification and is intended solely for research and educational purposes.
          </p>
          <p className="mb-4 leading-relaxed">
            The application uses the MobileViT-S deep learning architecture, trained on the ISIC 2020 dataset.
            This dataset contains dermoscopic images labelled for skin lesion classification and is known to be imbalanced.
          </p>

          <h2 className="text-2xl font-semibold mb-4 mt-6">Disclaimer</h2>
          <p className="mb-4 leading-relaxed">
            This application is an academic prototype and may contain coding errors, modelling limitations, or biases inherited from the training data.
            As a result, classifications produced by the system may be incorrect.
          </p>
          <p className="mb-4 leading-relaxed">
            The application does not provide a medical diagnosis, does not replace professional medical advice, and must not be used to make clinical decisions.
          </p>
          <p className="mb-4 leading-relaxed">
            If you are concerned about a skin lesion or any aspect of your health, you should consult a qualified healthcare professional.
          </p>

          <h2 className="text-2xl font-semibold mb-4 mt-6">Data Handling</h2>
          <p className="mb-4 leading-relaxed">
            Uploaded images are used only for the purpose of analysis within the application.
            No images or personal data are intentionally stored, shared, or used beyond the scope of this academic demonstration.
          </p>
        </div>

        <div className="bg-white p-8 rounded-xl shadow-sm my-8">
          {resultsContent}
        </div>
      </div>
      <SiteFooter />
    </div>
  );
}
export default AnalysisPage;