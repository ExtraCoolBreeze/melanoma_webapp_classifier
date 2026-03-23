#Name: Craig McMillan
#Student Number: 2390641
#Date: 14/03/26
#Training script for the MobileViT-S model

#importing required libraries
import os
import time
import pandas as pd
import torch
import torch.nn as nn
import cv2
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from transformers import AutoImageProcessor, MobileViTForImageClassification
from tqdm import tqdm

#setting file paths for loading inputs and saving outputs
modelWeights = "/Users/craig/Documents/GitHub/melanoma_webapp_classifier/model/hf/apple_mobilevit_small"
loadedCSV = "/Users/craig/Documents/GitHub/melanoma_webapp_classifier/data/cleaned_csv/cleanedGroundTruth_V2.csv"
imgDataset = "/Users/craig/Desktop/TrainingData/cleanedData_Final"
savedWeights = "/Users/craig/Documents/GitHub/melanoma_webapp_classifier/model/trained"

#setting main training variables for easy access
optimiserName = "adam"
learningRate = 5e-4
batchSize = 16
numEpochs = 10
patience = 5
threshold = 0.5
numWorkers = 0

#defining deviceSelection function to select best device based on platform
def deviceSelection():
    if torch.backends.mps.is_available() and torch.backends.mps.is_built():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")

#defining SkinLesionDataset class for loading images and labels from the dataset
class SkinLesionDataset(Dataset):

    #defining __init__ method for storing the loaded csv files, loading images and image preprocessor
    def __init__(self, loadedCSV, imgDataset, processor):
        self.csvData = loadedCSV.reset_index(drop=True)
        self.imgData = imgDataset
        self.processor = processor

    #defining __len__ function that returns total number of rows in the dataset
    def __len__(self):
        dataCount = len(self.csvData)
        return dataCount

    #defining __getitem__ function that loads a single image and label based on the index and processes the image
    def __getitem__(self, index):
        currentRow = self.csvData.iloc[index]
        targetLabel = int(currentRow["target"])
        filename = f"cleaned_{currentRow['image_name']}.jpg"
        imagePath = os.path.join(self.imgData, filename)
        loadedImage = cv2.imread(imagePath)

        #throws error if image cannot be loaded
        if loadedImage is None:
            raise FileNotFoundError(f"Error, could not load image {imagePath}")
        
        #processes images and returns tensors
        processedImage = self.processor(images=loadedImage, return_tensors="pt", do_resize=False, do_center_crop=False)["pixel_values"].squeeze(0)
        targetTensor = torch.tensor(targetLabel, dtype=torch.float32)
        return processedImage, targetTensor

#defines trainEpoch function that trains the model for a full epoch and returns averageLoss and accuracy
def trainEpoch(model, loader, optimiser, lossFunction, device):
    model.train()
    totalLoss = 0.0
    totalCorrect = 0
    totalImages = 0
    totalBatches = len(loader)

    #loops over each batch
    for batchNum, (inputs, labels) in enumerate(loader):
        inputs = inputs.to(device)
        labels = labels.to(device).unsqueeze(1)
        
        #added optimiser.zero_grad to improve performance
        optimiser.zero_grad()

        #calculating loss
        outputs = model(inputs).logits
        loss = lossFunction(outputs, labels)

        #updating weights
        loss.backward()
        optimiser.step()

        #counting total loss
        totalLoss += loss.item()

        #converting outputs into class predicitons
        predictions = (torch.sigmoid(outputs) >= threshold).long()
        totalCorrect += (predictions == labels.long()).sum().item()
        totalImages += labels.size(0)

        #print the patch progress every 50 batches to track progress
        if batchNum % 50 == 0:
            print(f"Batch {batchNum}/{totalBatches}")

    #calculates the average training loss and accuracy for the epoch and returns the values
    averageLoss = totalLoss / len(loader)
    accuracy = totalCorrect / totalImages
    return averageLoss, accuracy

#Defining validateEpoch function to evaluate model without updating model weights
#returns the average validation loss and accuracy
def validateEpoch(model, loader, lossFunction, device):
    model.eval()
    totalLoss = 0.0
    totalCorrect = 0
    totalImages = 0
    totalBatches = len(loader)

    #turning off gradient calculation during evaluation to use less memory
    with torch.no_grad():
        #loop over each batch
        for batchNum, (inputs, labels) in enumerate(loader):
            inputs = inputs.to(device)
            labels = labels.to(device).unsqueeze(1)
            
            #calculate validation loss
            outputs = model(inputs).logits
            loss = lossFunction(outputs, labels)
            totalLoss += loss.item()

            #converting outputs into class predictions
            predictions = (torch.sigmoid(outputs) >= threshold).long()
            totalCorrect += (predictions == labels.long()).sum().item()
            totalImages += labels.size(0)

            #print the patch progress every 50 batches to track progress
            if batchNum % 50 == 0:
                print(f"Batch {batchNum}/{totalBatches}")
    #calculate average loss and accuracy for each epoch and returns the values
    averageLoss = totalLoss / len(loader)
    accuracy = totalCorrect / totalImages
    return averageLoss, accuracy

#defining the main training method that load data, configures the model
#runs the training with the selected optimiser and saved the best model
def main():
    chosenDevice = deviceSelection()
    print(f"Chosen device {chosenDevice}")
    os.makedirs(savedWeights, exist_ok=True)
    cleanedCSV_df = pd.read_csv(loadedCSV)
    totalImages = len(cleanedCSV_df)
    targetBenign = (cleanedCSV_df["target"] == 0).sum()
    targetMalignant = (cleanedCSV_df["target"] == 1).sum()
    imbalanceRatio = targetBenign / targetMalignant

    #prints to confirm dataloading
    print(f"Csv file loaded from {loadedCSV}")
    print(f"The CleanedData_Final dataset contains {totalImages} images in total. {targetBenign} benign and {targetMalignant} malignant images. Imbalance ratio {imbalanceRatio}")

    #set file paths for the train, test and validation splits
    trainSplitPath = os.path.join(savedWeights, "train_split.csv")
    testSplitPath = os.path.join(savedWeights, "test_split.csv")
    validationSplitPath = os.path.join(savedWeights, "validation_split.csv")
    
    #checks if split files already exist 
    splitsExist = os.path.exists(trainSplitPath) and os.path.exists(testSplitPath) and os.path.exists(validationSplitPath)

    #if splits exist load files
    if splitsExist:
        train_df = pd.read_csv(trainSplitPath)
        test_df = pd.read_csv(testSplitPath)
        validate_df = pd.read_csv(validationSplitPath)
        print("split csv files found, loading files")
    else:
        #else create and save new splits
        uniquePatients = cleanedCSV_df["patient_id"].unique()
        trainPatients, tempTestPatients = train_test_split(uniquePatients, test_size=0.30, random_state=42)
        validatePatients, testPatients = train_test_split(tempTestPatients, test_size=0.50, random_state=42)
        train_df = cleanedCSV_df[cleanedCSV_df["patient_id"].isin(trainPatients)].reset_index(drop=True)
        test_df = cleanedCSV_df[cleanedCSV_df["patient_id"].isin(testPatients)].reset_index(drop=True)
        validate_df = cleanedCSV_df[cleanedCSV_df["patient_id"].isin(validatePatients)].reset_index(drop=True)
        #saving new split files
        train_df.to_csv(trainSplitPath, index=False)
        test_df.to_csv(testSplitPath, index=False)
        validate_df.to_csv(validationSplitPath, index=False)
        print("No csv files found, splits created using random_state=42 for reproducibility and saved file")
    #print the results of the train test split
    print(" ")
    print("Patient level split applied based on data analysis using a 70/30, with 30 spit evenly between test and validation sets")
    print(f"Training set: {len(train_df)} images with {train_df['target'].sum()} malignant cases")
    print(f"Test set: {len(test_df)} images with {test_df['target'].sum()} malignant cases")
    print(f"Validation: {len(validate_df)} images with {validate_df['target'].sum()} malignant cases")
    print(" ")

    #load the image processor with the pretrained weights
    processor = AutoImageProcessor.from_pretrained(modelWeights, use_fast=False)

    #load the pretrained model and get the existing classifier feature input size
    model = MobileViTForImageClassification.from_pretrained(modelWeights)
    inputFeatures = model.classifier.in_features
    
    #configure the classifier for binary classification
    model.classifier = nn.Linear(inputFeatures, 1)
    model = model.to(chosenDevice)

    #loading the data for training
    trainLoader = DataLoader(
        SkinLesionDataset(train_df, imgDataset, processor),
        batch_size=batchSize,
        shuffle=True,
        num_workers=numWorkers
    )
    #loading the data for validation
    validationLoader = DataLoader(
        SkinLesionDataset(validate_df, imgDataset, processor),
        batch_size=batchSize,
        shuffle=False,
        num_workers=numWorkers
    )

    #calculating the positive weighting target for minority class
    benignCount = (train_df["target"] == 0).sum()
    malignantCount = (train_df["target"] == 1).sum()
    positiveWeightValue = torch.tensor([benignCount / malignantCount], dtype=torch.float32)
    positiveWeight = positiveWeightValue.to(chosenDevice)

    #setting loss function and class weighting for minority class
    lossFunction = nn.BCEWithLogitsLoss(pos_weight=positiveWeight)
    print(f"The loss function has been set to BCEWithLogitsLoss along with postive weight of {positiveWeight.item():.1f} asigned to address the class imbalance")
    print(" ")
    #select optimiser used in training based on name chosen for training cycle
    if optimiserName == "adam":
        selectedOptimiser = torch.optim.Adam(model.parameters(), lr=learningRate)
    elif optimiserName == "rmsprop":
        selectedOptimiser = torch.optim.RMSprop(model.parameters(), lr=learningRate)
    elif optimiserName == "sgd":
        selectedOptimiser = torch.optim.SGD(model.parameters(), lr=learningRate)
    #print the optimiser selected and the learning rate applied
    print(f"{optimiserName} selected with a learning rate of {learningRate}")
    print(" ")
    #set values for tracking validation and training history
    bestValLoss = float("inf")
    bestValAcc = 0.0
    bestEpoch = 0
    earlyStopCount = 0
    history = {"epoch": [], "trainingloss": [], "validationloss": [], "trainingAccuracy": [], "validationAccuracy": [], "epoch_time_mins": []}

    #print training configuration to remove check for incorrect configuration
    print("--")
    print(f"Beginning training with the {optimiserName} optimiser")
    print(f"The model will train for a maximum of {numEpochs} epochs")
    print(f"Each batch contains {batchSize} images")
    print(f"Early stopping is enabled with a patience of {patience} epochs")
    print(f"Data loading is using {numWorkers} worker processes")
    print("--")

    #saving the total training time
    trainingStartTime = time.time()
    #loop over each training epoch
    for epoch in tqdm(range(numEpochs), desc="Epochs"):
        epochStartTime = time.time()
        #trainind model for 1 epoch then validating for 1 epoch
        trainLoss, trainAccuracy = trainEpoch(model, trainLoader, selectedOptimiser, lossFunction, chosenDevice)
        valLoss, valAccuracy = validateEpoch(model, validationLoader, lossFunction, chosenDevice)
        #calculate time taken for each epoch
        epochTime = time.time() - epochStartTime
        epochTimeMins = epochTime / 60
        #adds 1 to epoch count to keep accurate count as code starts from o
        epochNum = epoch + 1

        #save training history for later testing and evaluation
        history["epoch"].append(epochNum)
        history["trainingloss"].append(round(trainLoss, 4))
        history["validationloss"].append(round(valLoss, 4))
        history["trainingAccuracy"].append(round(trainAccuracy, 4))
        history["validationAccuracy"].append(round(valAccuracy, 4))
        history["epoch_time_mins"].append(round(epochTimeMins, 1))
        
        #print information summary after each epoch completes
        print("--")
        print(f"Epoch {epochNum} of {numEpochs} completed in {epochTimeMins:.1f} minutes")
        print(f"Training loss: {round(trainLoss, 4)} with an accuracy of {round(trainAccuracy, 4)}")
        print(f"Validation loss: {round(valLoss, 4)} with an accuracy of {round(valAccuracy, 4)}")
        print("--")

        #if validation loss has improved save the data from that epoch
        if valLoss < bestValLoss:
            previousBestValLoss = bestValLoss
            bestValLoss = valLoss
            bestValAcc = valAccuracy
            bestEpoch = epochNum
            earlyStopCount = 0
            savePath = os.path.join(savedWeights, f"best_{optimiserName}.pth")
            #saves the model data when best validation loss is calculated
            torch.save({
                "epoch": epochNum,
                "state_dict": model.state_dict(),
                "val_loss": valLoss,
                "val_accuracy": valAccuracy,
                "optimiser_name": optimiserName
            }, savePath)
            print(f"Validation loss improved from {round(previousBestValLoss, 4)} to {round(valLoss, 4)}. New best model at epoch {epochNum}")
        else:
            #increases the early stop counter and if limit is reached, stops training early
            earlyStopCount += 1
            print(f"Validation loss did not improve. No improvement for {earlyStopCount} of {patience} allowed epochs. Continuing will risk overfitting")
            if earlyStopCount >= patience:
                print(f"Stopped early at {epochNum} to prevent overfitting. Best model found at epoch {bestEpoch}")
                break

        print("---")

    #records the total training time for later use
    totalTrainingTime = time.time() - trainingStartTime

    #print the training summary
    print("--")
    print(f"Training complete using {optimiserName}. Time: {totalTrainingTime / 60:.1f}")
    print("---")
    print(f"Training Loss: {round(trainLoss, 4)}")
    print(f"Validation Loss: {round(valLoss, 4)}")
    print(f"Training Accuracy: {round(trainAccuracy, 4)}")
    print(f"Validation Accuracy: {round(valAccuracy, 4)}")
    print("--")

    #print best performance validation results
    print("Best Model Performance")
    print("---")
    print(f"Best Validation Loss: {round(bestValLoss, 4)}")
    print(f"Best Validation Accuracy: {round(bestValAcc, 4)}")
    print(f"Best Epoch: {bestEpoch}")
    print("--")
    
    #print whether training stopped or completed
    if epoch + 1 < numEpochs:
        print(f"Training stopped after {epoch + 1} epochs. patience = {patience}")
    else:
        print(f"All {numEpochs} epochs completed")
    print("---")
    
    #save history as a csv file for use in testing and validation
    historyDf = pd.DataFrame(history)
    historyCsvPath = os.path.join(savedWeights, f"history_{optimiserName}.csv")
    historyDf.to_csv(historyCsvPath, index=False)
    print(f"Training history saved to {historyCsvPath}")

#Allows the file to be run as a script
if __name__ == "__main__":
    main()