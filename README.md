# Spot Check Medical

Spot Check Medical is a 4th year university project focused on developing a deep learning-based web application for melanoma detection and classification. The system analyses dermoscopic images and predicts whether a lesion is benign or malignant. It uses the MobileViT-S architecture, the ISIC 2020 dataset, and a custom implementation of the DullRazor preprocessing algorithm.

## How to set up and run the program

Use the comments below in the terminal in VS Code

### Code To Install Dependencies

pip install -r requirements.txt 

### Code to Start Backend 

uvicorn main:app --reload

## Code to Start Frontend

npm install
npm run dev