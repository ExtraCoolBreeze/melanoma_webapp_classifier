import { useNavigate } from "react-router-dom";

function ResultsPage() {
  const navigate = useNavigate();

  function handleGoBackClick() {
    navigate("/");
  }

  return (
    <div>
      <h1>Analysis Results</h1>

      <p>The results of the analysis will be shown here.</p>

      <button onClick={handleGoBackClick}>
        Back
      </button>
    </div>
  );
}

export default ResultsPage;
