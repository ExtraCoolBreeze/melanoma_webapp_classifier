#importing libraries
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.dullrazor import image_preprocessing
from backend.modelvit import modelPredict 
import cv2
from PIL import Image
from io import BytesIO
import numpy as np

#starting fast api
app = FastAPI()

#configuring middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#defining accepted file extensions
acceptedFileExtensions = {".jpg", ".jpeg", ".png"}

#confirming that backend is running
@app.get("/")
def root():
    return {"message": "Backend is running"}

    #defining predict endpoint 
@app.post("/predict")
#defining predictsImage function that acepts uploaded files
async def predictImage(file: UploadFile = File(...)):

    #validating the file extension before processing
    fileName = file.filename.lower()
    validFile = False
    #loops over acceptedFilesExtensions to validate image
    for extension in acceptedFileExtensions:
        if fileName.endswith(extension):
            validFile = True
    if not validFile:
        raise HTTPException(status_code=400, detail="Image file format unsupported. Please upload a jpg, jpeg, or png image")

    #reading the uploaded file
    readImage = await file.read()

    #opening the uploaded image
    openedImage = Image.open(BytesIO(readImage))

    #converting to rgb as for processing by np.array
    convertedImageRGB = openedImage.convert("RGB")

    #converting the image to array
    imageArray = np.array(convertedImageRGB)

    #converting the image from rgb to bgr as dullrazor image_preprocessing expects bgr 
    bgrImage = cv2.cvtColor(imageArray, cv2.COLOR_RGB2BGR)

    #preprocessing image 
    processedDullrazorImage = image_preprocessing(bgrImage)

    #sending image to model for prediction
    predictionResult = modelPredict(processedDullrazorImage)
    
    #returning the prediction
    return predictionResult
