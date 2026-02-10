import { useNavigate } from "react-router-dom";

function HomePage() {
  const navigate = useNavigate();

  function handleAnalyseClick() {
    // For now, just navigate to the results page
    navigate("/analysis");
  }

  return (
    <div>
      <h1>Spot Check Medical</h1>

      <button onClick={handleAnalyseClick}>
        Analyse Image
      </button>
    </div>
  );
}

export default HomePage;
