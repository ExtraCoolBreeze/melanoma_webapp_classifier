import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import SiteHeader from "../components/header";
import SiteFooter from "../components/footer";

function HomePage() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [imageUrl, setImageUrl] = useState("");
  const [fileName, setFileName] = useState("");
  const [isLoading, setIsLoading] = useState(false);


  function handleUploadClick() {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  }

  function handleFileChange(event) {
    const file = event.target.files[0];
    if (!file) {
      return;
    }

    const localUrl = URL.createObjectURL(file);
    setImageUrl(localUrl);
    setFileName(file.name);
    setError("")
  }

  
  const [error, setError] = useState("");

  async function handleAnalyseClick() {
    if (!imageUrl) {
      setError("Please upload an image for analysis");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const file = fileInputRef.current.files[0];

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("cannot retreive analysis data");
      }

      const predictionData = await response.json();

      navigate("/analysis", {
        state: {
          predictionData: predictionData,
          imageUrl: imageUrl,
          fileName: fileName,
        },
      });
    } catch (err) {
      console.error("error", err);
      setError("Could not analyse image");
    } finally {
      setIsLoading(false);
    }
  }

  let imageDisplay;
  if (imageUrl) {
    imageDisplay = ( <img src={imageUrl} alt="Uploaded image" className="max-w-full max-h-full object-contain"/>);
  } else {
    imageDisplay = ( <span className="text-black font-medium">Uploaded Image</span> );
  }

  let fileNameDisplay;
  if (fileName) {
    fileNameDisplay = fileName;
  } else {
    fileNameDisplay = "File Name";
  }

  return (

    <div className="min-h-screen flex flex-col bg-[#005EB8]">
      <SiteHeader />

      <div className="w-full py-8 flex-1">
        <div className="bg-white p-8 my-8 text-black">
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
        <div className="h-0.5 bg-linear-to-r from-transparent via-navy-blue to-transparent my-8" />
        <div className="bg-white p-8 shadow-sm my-8">
          <div className="flex justify-center my-8">
            <div>
              <div className="w-100 h-100 border-2 border-gray-300 flex items-center justify-center overflow-hidden bg-light-gray">
                {imageDisplay}
              </div>
              <div className="text-center mt-2 font-medium text-black text-sm">
                {fileNameDisplay}
              </div>
            </div>
          </div>

          <input ref={fileInputRef} type="file" accept="image/*" onChange={handleFileChange} className="hidden"/>
          {error && (
            <div className="text-center mb-4 text-red-600 font-semibold">
              {error}
            </div>
          )}

          <div className="flex gap-4 justify-center mt-8">
            <button className="bg-[#005EB8] hover:opacity-90 text-white font-semibold px-8 py-3 rounded-lg transition-opacity underline" onClick={handleUploadClick}>
              Upload
            </button>

            <button className="bg-[#005EB8] hover:opacity-90 text-white font-semibold px-8 py-3 rounded-lg transition-opacity underline" onClick={handleAnalyseClick}>
              Analyse
            </button>
          </div>
        </div>
        <div className="h-0.5 bg-linear-to-r from-transparent via-navy-blue to-transparent my-8" />
      </div>
      <SiteFooter />
    </div>
  );
}

export default HomePage;