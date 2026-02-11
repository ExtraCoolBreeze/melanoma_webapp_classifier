from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is running"}

    # predicion test
@app.post("/predict")
def predictImage(file: UploadFile = File(...)):

    return {
        "label": "melanoma",
        "confidence": 0.01,
        "probabilities": {
            "melignant": 0.99,
            "benign": 0.40
        }
    }