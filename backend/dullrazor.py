#Name: Craig McMillan
#Student Number: 2390641
#Date: 14/03/26
#DullRazor script for image preprocessing inlcudes hair removal, image padding and resizing to fit model input size.

#import cv2 and pathlib
import cv2
from pathlib import Path

#defining accepted file extensions 
acceptedfileExtensions = {".jpg", ".jpeg", ".png"}

#defining image_preprocessing function that accepts an image, removes hair, pads to a square, resizes it to 256x256 and returns the resized image
def image_preprocessing(acceptedImage):

    #getting output of dullrazor function
    processedImage = dullrazor(acceptedImage)

    #get the original image dimensions
    originalHeight, originalWidth = processedImage.shape[:2]

    #set square size using height and width
    squareSize = max(originalHeight, originalWidth)

    #calculate padding
    heightPadding = squareSize - originalHeight
    widthPadding = squareSize - originalWidth

    #calculate padding for each side of square
    topPad = heightPadding // 2
    bottomPad = heightPadding - topPad
    leftPad = widthPadding // 2
    rightPad = widthPadding - leftPad

    #pad image to square using a black border
    paddedImage = cv2.copyMakeBorder(processedImage, topPad, bottomPad, leftPad, rightPad, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    #set target size for model input
    targetSize = 256

    #resize padded square image using INTER_LANCZOS4 for downsizing
    resizedImage = cv2.resize(paddedImage, (targetSize, targetSize), interpolation=cv2.INTER_LANCZOS4)

    #return the resized image
    return resizedImage

#defining the dullrazor function along with passing the image and tested parameters,
#applies greyscale, a blackhat transformation, binary masking and then inpaints
# before returning the final cleaned image
def dullrazor(acceptedImage, lowbound=10, showimgs=False, filterstruc=9, inpaintmat=6):

    #converting colour from BGR to grayscale for hair detection
    grayscaleImage = cv2.cvtColor(acceptedImage, cv2.COLOR_BGR2GRAY)

    #setting filter size and kernel used to detect hair
    filterSize = (filterstruc, filterstruc)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, filterSize)

    #applying blackhat morphological transformation to isolate dark hairs
    transformedImage = cv2.morphologyEx(grayscaleImage, cv2.MORPH_BLACKHAT, kernel)
    
    #adding blur to blackhat mask to reduce image noise to smooth out details before thesholding
    blackhatBlur = cv2.GaussianBlur(transformedImage, (3,3), 0)

    #Adding threshold to correct binary blurred mask to 0 & 255 binary. 0 = skin and 255 = hair
    _, mask = cv2.threshold(blackhatBlur, lowbound, 255, cv2.THRESH_BINARY)


    #inpainting the hair located using the binary mask
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

#defining main method
def main():

    #set location of image to process and save
    newImageDir = Path ("/Volumes/USB DRIVE/ISIC2020Data/TrainingData/ISIC_2020_Training_JPEG/train/")
    savedImageDir = Path ("/Users/craig/Desktop/TrainingData/cleanedData_Final")

    #checking if the directory exists, if not creating the directory
    savedImageDir.mkdir(parents=True, exist_ok=True)

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
        
        #set new cleaned file name
        cleanedfileName = f"cleaned_{imagePath.name}"

        #set full file path and directory
        savedfilePath = savedImageDir / cleanedfileName

        if savedfilePath.exists():
            print(f"[{index}/{imageCount}] File {cleanedfileName} already processed, skipping file")
            continue

        #get output of processed image
        loopOutput = image_preprocessing(imageinLoop)

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

#this allows the file to be run as a script
if __name__ == "__main__":
    main()