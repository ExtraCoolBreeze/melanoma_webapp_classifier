#import cv2 and pathlib
import cv2
from pathlib import Path
#set location of image to process and save
newImageDir = Path ("/Volumes/USB DRIVE/ISIC2020Data/TrainingData/ISIC_2020_Training_JPEG/train/")
savedImageDir = Path ("/Volumes/USB DRIVE/ISIC2020Data/TrainingData/cleanedData")

#defining accepted file extensions 
acceptedfileExtensions = {".jpg", ".jpeg", ".png"}

#checking if the directory exists, if not creating the directory
savedImageDir.mkdir(parents=True, exist_ok=True)

#image_processing function that accepts an image
def image_preprocessing(acceptedImage):

    # removing hairs using dullrazor function
    processedImage = dullrazor(acceptedImage)
    return processedImage

#defining the dullrazor function along with passing variables
def dullrazor(acceptedImage, lowbound=10, showimgs=False, filterstruc=9, inpaintmat=6):

    # corrected colour change BGR to grayscale
    grayscaleImage = cv2.cvtColor(acceptedImage, cv2.COLOR_BGR2GRAY)

    # applying a blackhat morphological operation
    #set filter size
    filterSize = (filterstruc, filterstruc)

    #set kernal size
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, filterSize)

    #applying black hat transformation
    transformedImage = cv2.morphologyEx(grayscaleImage, cv2.MORPH_BLACKHAT, kernel)
    
    #adding blur to blackhat mask to smooth out details
    blackhatBlur = cv2.GaussianBlur(transformedImage, (3,3), 0)

    # 0 = skin and 255 = hair
    #Adding threshold to correct binary blurred mask to 0 & 255 binary
    ret, mask = cv2.threshold(blackhatBlur, lowbound, 255, cv2.THRESH_BINARY)


    # inpainting using the mask
    finalImage = cv2.inpaint(acceptedImage, mask, inpaintmat, cv2.INPAINT_TELEA)

    #display all images using imshow and return final cleaned image
    if showimgs:
        print("_____DULLRAZOR_____")
        cv2.imshow("Gray", grayscaleImage)
        cv2.imshow("Blackhat", transformedImage)
        cv2.imshow("Mask", mask)
        cv2.imshow("Final Cleaned Image", finalImage)
        print("___________________")
    return finalImage

#set imageBatch array
imageBatch = []

#looping over each file in the file directory, if accepted file extension add to array
for filePath in newImageDir.iterdir():
    if filePath.suffix.lower() in acceptedfileExtensions:
        imageBatch.append(filePath)

#Sorting Order of batch files
imageBatch.sort()

#count the length of the array
imageCount = len(imageBatch)

#for each index in array
for index, imagePath in enumerate(imageBatch, start=1):
    #read image to imageinLoop to validate and print accepted image
    imageinLoop = cv2.imread(str(imagePath))
    if imageinLoop is None:
        print(
            f"[{index}/{imageCount}] "
            f"could not load "
            f"{imagePath.name}"
        )
        continue
    
    #current image output from loop
    loopOutput = image_preprocessing(imageinLoop)

    #set new cleaned file name
    cleanedfileName = f"cleaned_{imagePath.name}"

    #set full file path and directory
    savedfilePath = savedImageDir / cleanedfileName

    #save image
    comfirmedImage = cv2.imwrite(str(savedfilePath), loopOutput)
    if not comfirmedImage:
        print(f"[{index}/{imageCount}] "
        f"Failed to save {savedfilePath.name}"
        )
        continue


    #calculate progress percent and print message
    progressPercent = (index / imageCount) * 100
    print(
    f"[{index}/{imageCount}] "
    f"({progressPercent:.1f}%) "
    f"Saved: {savedfilePath.name}"
    )
#print complete message
print("Dullrazor processing complete")