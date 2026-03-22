#Name: Craig McMillan
#Student Number: 2390641
#Date: 14/03/26
# This file loads the MobileViT-s model with pretrained weights, replaces the classifier for binary classification, 
# applies the best trained model weights, and defines the modelPredict function used by the FastAPI backend for inference.


#importing libraries
from transformers import AutoImageProcessor, MobileViTForImageClassification
import torch
import torch.nn as nn

#setting file path loading in weights and best trained model
modelWeights = "/Users/craig/Documents/GitHub/melanoma_webapp_classifier/model/hf/apple_mobilevit_small"
trainedModel = "/Users/craig/Documents/GitHub/melanoma_webapp_classifier/model/trained/best_sgd.pth"

#defining deviceDelection function to select best device based on platform
def deviceSelection():
    if torch.backends.mps.is_available() and torch.backends.mps.is_built():
      return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")

#choosing the best device based on above function output and printing result
chosenDevice = deviceSelection()
print(f"Device selected {chosenDevice}")

#loading default processor configuration
imageProcessor = AutoImageProcessor.from_pretrained(modelWeights, use_fast=False)

#load model and classifier with binary classification
classificationModel = MobileViTForImageClassification.from_pretrained(modelWeights)
inputFeatures = classificationModel.classifier.in_features
classificationModel.classifier = nn.Linear(inputFeatures, 1)

#load saved model, applying weights and set for evaluation
savedModel = torch.load(trainedModel, map_location=chosenDevice, weights_only=False)
classificationModel.load_state_dict(savedModel["state_dict"])
classificationModel = classificationModel.to(chosenDevice)
classificationModel.eval()

#printing model information to view correct configuration
print(f"Processor loaded", imageProcessor)
print(f"Loaded trained weights from {trainedModel}")
print("Model image size:", classificationModel.config.image_size)
print("Classifier head: ", classificationModel.classifier)

#defining modelPredict function which accepts a preprocessed image, puts it through the the model,
#converts the logit result to a probability using sigmoid, and returns the classification, confidence score and class probabilities
def modelPredict(preprocessedImage):
    #setting threshold
    threshold = 0.5

    #processing image
    processedInputs  = imageProcessor(images=preprocessedImage, return_tensors="pt", do_resize=False, do_center_crop=False)
    modelInput = processedInputs["pixel_values"].to(chosenDevice)

     #turning off gradient calculation to use less memory
    with torch.no_grad():
        outputs = classificationModel(modelInput)
        modelOutput = outputs.logits
        #applying .squeeze() to remove dimentions from tensor
        squeezedOutput = modelOutput.squeeze()
    
    #converting logit into malignant score
    malignantScore = torch.sigmoid(squeezedOutput).item()
    benignScore = 1.0 - malignantScore
    
    #classifying based on threshold
    if malignantScore >= threshold:
        classLabel = "Malignant"
        confidenceScore = malignantScore
    else:
        classLabel = "Benign"
        confidenceScore = benignScore

    #rounding the scores for a more readable output in the frontend
    roundedMalignant = round(malignantScore, 2)
    roundedBenign = round(benignScore, 2)
    roundedConfidence = round(confidenceScore, 2)

    #creating prediction result dictionary
    predictionResult = {
        "label": classLabel,
        "confidence": roundedConfidence,
        "probabilities":{
        "malignant": roundedMalignant,
        "benign": roundedBenign,
        }
    }

    #returning the prediction reuslts
    return predictionResult