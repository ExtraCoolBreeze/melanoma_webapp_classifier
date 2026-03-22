//Name: Craig McMillan
//Student Number: S2390641
//Date: 14/03/26
//The analysis page receives the analysis output from the backend and displays the prediction, confidence and probability scores, along with a bar chart

//importing react routing
import { useLocation, useNavigate } from "react-router-dom";
import SiteHeader from "../components/header";
import SiteFooter from "../components/footer";
import { useEffect, useRef } from "react";
import Chart from 'chart.js/auto';

//entry point for the page
function AnalysisPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  //These variables stores the prediction data, image url and file name passed from the home page
  let predictionData = null;
  let imageUrl = null;
  let fileName = null;

  if (location.state) {
    predictionData = location.state.predictionData;
    imageUrl = location.state.imageUrl;
    fileName = location.state.fileName;
  }

  //this variable stores the confidence score 
  let confidencePercent = null;
  if (predictionData) {
    //converts the confidence score to a percentage for display
    confidencePercent = predictionData.confidence * 100;
  }

  //useEffect function creates the chart, displays chart data, and destroys the chart display
  useEffect(() => {
    if (predictionData && chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      const ctx = chartRef.current.getContext('2d');

      const benignProb = predictionData.probabilities.benign * 100;
      const malignantProb = predictionData.probabilities.malignant * 100;

      chartInstance.current = new Chart(ctx, {
        type: 'bar',

        data: {
          labels: ['Benign', 'Malignant'], 
          datasets: [{
            label: 'Probability (%)', 
            data: [benignProb, malignantProb],
            backgroundColor: ['rgba(34, 197, 94, 0.8)', 'rgba(239, 68, 68, 0.8)'],
            borderColor: ['rgba(34, 197, 94, 1)', 'rgba(239, 68, 68, 1)'],
            borderWidth: 2
          }]
        },

        options: {
          responsive: true,
          maintainAspectRatio: false,

          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              ticks: { color: '#000000',weight: 'bold', callback(value) {
                 return value + '%'; 
                } },
              grid: { color: '#000000', weight: 'bold'}, title: { display: true, text: 'Probability (%)', color: '#000000', font: { size: 14, weight: 'bold' } }
            },

            x: {
               ticks: { color: '#000000', weight: 'bold'}, grid: { color: '#000000'}, title: { display: true, text: 'Classification', color: '#000000', font: { size: 14, weight: 'bold' } } }
          },

          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label(context) {
                  return 'Probability: ' + context.parsed.y + '%'; 
                }
              }
            }
          }
        }
      });

    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [predictionData]);

  //resultsContent variable 
  let resultsContent;
  
  //Displays the results section without prediction data if no data was received
  if (!predictionData) {
    resultsContent = (
      <div>
        <h1 className="text-5xl font-normal leading-tight mb-6">Analysis Results</h1>
        <div className="flex gap-4 justify-center mt-8">
          <button className="bg-[#005EB8] hover:opacity-90 text-white font-semibold px-8 py-3 rounded-lg transition-opacity underline" onClick={() => navigate("/")}>
            Go back
          </button>
        </div>
      </div>
    );
  } else {

    let displayFileName = "Uploaded Image";
    if (fileName) {
      displayFileName = fileName;
    }

    let imageDisplay;
    if (imageUrl) {
      imageDisplay = (
        <img src={imageUrl} alt="Uploaded image" className="max-w-full max-h-full object-contain" />
      );
    } else {
      imageDisplay = <span className="text-black font-medium">Uploaded Image</span>;
    }

    let fileNameDisplay;
    if (fileName) {
      fileNameDisplay = fileName;
    } else {
      fileNameDisplay = "File Name";
    }

    //populates the results layout with the image analysis data
    resultsContent = (
      <div>
        <h1 className="text-5xl font-normal leading-tight mb-4">Analysis Results</h1>
        <div className="flex flex-col md:flex-row gap-8 mb-8">
          <div className="md:w-1/2">
            <div className="w-full h-80 border-2 border-gray-300 flex items-center justify-center overflow-hidden bg-[#EDEEEE]">
              {imageDisplay}
            </div>
            <div className="text-center mt-2 font-medium text-black text-sm">
              {fileNameDisplay}
            </div>
          </div>

          <div className="md:w-1/2">
            <div className="w-full h-80">
              <canvas ref={chartRef}></canvas>
            </div>
            <div className="text-center mt-2 font-medium text-black text-sm">
              Class Probability Distribution
            </div>
          </div>
        </div>

      <div className="flex flex-col md:flex-row gap-8 mb-8">
        <div className="md:w-1/2 p-4 rounded">
          <h3 className="text-lg font-semibold mb-3">Classification Prediction</h3>
          <p className="mb-3 leading-relaxed">
            The image displayed above has been analysed using the MobileViT-S deep learning model integrated within this application. 
            The model evaluates visual patterns within the dermoscopic image and produces a classification indicating whether the lesion is predicted to be benign (non-cancerous) or malignant (potentially cancerous).
          </p>
          <p className="mb-3 leading-relaxed">
            For this particular image, the model has predicted: {predictionData.label}.
          </p>
          <p className="mb-3 leading-relaxed">
            This result is accompanied by a confidence score of {confidencePercent}%.
          </p>
          <p className="mb-0 leading-relaxed">
            The confidence score shows how sure the model is about its prediction. A higher percentage means the model believes the image is much more likely to belong to one category than the other.
            A lower percentage means the model sees similarities with both categories and is less certain about its decision.
            For example, a confidence score close to 100% means the model strongly favours one outcome, whereas a score closer to 50% means the model is not confident in either option. A very low value, such as 1%, would mean the model considers that classification extremely unlikely.
            It is important to understand that confidence reflects how certain the model is in its own calculation, and that this does not guarantee that the prediction is medically correct. Even high confidence scores can still be wrong.
          </p>
        </div>

        <div className="md:w-1/2 p-4 rounded">
          <h4 className="text-lg font-semibold mb-3">Understanding the Chart</h4>
          <p className="mb-3 leading-relaxed">
            The bar chart above shows a simple graphical visual that uses rectangular bars to compare values across categories.
            In this case, it is used to visually communicate the models estimated probabilities, making the results easier to interpret at a glance.
          </p>
          <p className="mb-3 leading-relaxed">
            The bar chart above represents:
          </p>
          <p className="mb-3 leading-relaxed">
            <strong className="text-green-600">Benign (Green):</strong> The probability that the lesion is non-cancerous.
          </p>
          <p className="mb-3 leading-relaxed">
            <strong className="text-red-600">Malignant (Red):</strong> The probability that the lesion is potentially cancerous
          </p>
          <p className="mb-3 leading-relaxed">
            The height of each bar corresponds to the probability assigned to that class by the model. 
            The taller bar indicates which classification the model considers more likely for the analysed image.
          </p>
          <p className="mb-0 leading-relaxed">
            These probability values illustrate how the model distributes its certainty between the two outcomes. They are influenced by the characteristics of the input image, the quality of the data, and the learned feature representations within the MobileViT architecture.
            As this is a binary classification task, the two probabilities will always sum to a total of 100%, reflecting the models allocation of confidence across the available classes.
          </p>
        </div>
      </div>

      <div className="p-4 rounded mb-8">
        <h4 className="text-lg font-semibold mb-3">Limitations of These Results</h4>
        <p className="mb-3 leading-relaxed">
          The results shown above are produced by an trained deep learning model and should not be interpreted as a medical diagnosis.
          This model provides a prediction based on patterns learned from training data and does not considered medical advice. Only a qualified healthcare professional can make a formal diagnosis following proper clinical assessment.
        </p>
        <p className="mb-3 leading-relaxed">
          The confidence score and probability values reflect how certain the model is in its prediction, not how medically accurate the result is. 
          A high confidence score does not guarantee correctness, as deep learning models can still make errors, particularly when analysing images that differ from the those selected used during training.
        </p>
        <p className="mb-3 leading-relaxed">
          The probabilities shown are estimates derived from the training dataset and the MobileViT-S architecture. They do not represent a confirmed medical diagnosis and may be influenced by dataset imbalance, image quality, and model limitations. 
          This application is an academic prototype intended for research and educational use and does not replace professional medical examination or diagnostic procedures.
        </p>
      </div>

        <div className="flex gap-4 justify-center mt-8">
          <button className="bg-[#005EB8] hover:opacity-90 text-white font-semibold px-8 py-3 rounded-lg transition-opacity underline" onClick={() => navigate("/")}>
            Go Back
          </button>
        </div>
      </div>
    );
  }

  //renders the about, disclaimer, and data handling page content. Also displays the resultsContent section
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

        <div className="bg-white p-8 shadow-sm my-8">
          {resultsContent}
        </div>
      </div>
      <SiteFooter />
    </div>
  );
}

export default AnalysisPage;