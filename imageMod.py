import time
import cv2
import os

#This is where the base directory for the files will be located
BASEDIR = 'D:\\Pictures\\'

#Where to get the images from, they can be the same if you want. NOTE: They will be added to BASEDIR 
INPUT, OUTPUT = 'Backgrounds\\', 'BackgroundOut\\'

#Name of the file that will be a backkdrop for the edges. NOTE: this wants to be equal to or greater than the next res else it may stretch it
COLOURTARGET = 'colour.jpg'

#Min Res you want an image to be. NOTE: 4K will cause opencv to fail
XRES, YRES = 2560, 1080

errorRep = []

target = BASEDIR + INPUT
targets = [] #list of all the file inputs

if target[-1] == "\\":
    #Cycle through the folder grabbing any valid pictures 
    for entry in os.scandir(target):
        if not entry.path.endswith("Outline.jpg") and (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():
            targets.append(entry.path)
    
else :
    print("Invalid Input")
    #how do end program

target = BASEDIR + OUTPUT #input("Either enter the path, or relative path to the picture. (a directory will do all files within)\n")
completedImages = {}

if target[-1] == "\\":
    # cycle through the out folder to see what exists
    for entry in os.scandir(target):
        if entry.path.endswith(".jpg") and entry.is_file():
            print(entry.name.split('.')[0])
            completedImages[entry.name.split('.')[0]] = True
else:
    print("Invalid Output")
    #need to end here

os.chdir(BASEDIR + OUTPUT)


for i, imgLoc in enumerate(targets):
    #each run is caught if it fails so the whole folder will atleast be attempted
    try:
        #basic variables to make future statements easier 
        startTime = time.time()
        imgFile = imgLoc.split('\\')   
        imgName = imgFile[-1].split('.')
        imgSave = imgName[0] + 'Outline' + ".jpg"
        
        #lets you know where the code currently is
        print("--------------------------------------")
        print("Reading: " + imgName[0])
        print('Completed: ', i, ' / ', len(targets))
        
        #skip the image if it has been found in the output already
        if completedImages.get(imgSave.split('.')[0], False):
            print('Operation time:', time.time() - startTime, 'secs')
            continue
        
        #renames the file if it was found prior and the in and out aren't using the same file.
        if INPUT != OUTPUT and completedImages.get(imgName[0], False):
            os.rename(target + imgName[0] + '.jpg', target + imgSave)
            print('Operation time:', time.time() - startTime, 'secs')
            continue
        
        ogImg = cv2.imread(imgLoc)

        #finds out if the image if bigger than the cap, and if so by what ratio to resize by
        ratio =  min(XRES / ogImg.shape[1], YRES / ogImg.shape[0])
        
        if ratio < 1:
            ogImg = cv2.resize(ogImg, (int(ogImg.shape[1] * ratio), int(ogImg.shape[0] * ratio)))
        
        #prepping the colour image with the right sizes        
        colour = cv2.imread(BASEDIR + COLOURTARGET)
        colour = cv2.resize(colour, (ogImg.shape[1], ogImg.shape[0]))

        #Getting the weak and strong threshold for the canny function
        gray = cv2.cvtColor(ogImg, cv2.COLOR_BGR2GRAY)
        histogram = cv2.calcHist([gray], [0], None, [256], [0,256])
        
        count = 0
        cutOff = 0.05 * ogImg.shape[1] * ogImg.shape[0]
        
        for i in reversed(range(len(histogram))):
                        
            count += histogram[i][0]
            
            if cutOff < count:
                lowThresh = int(0.45 * i)
                maxThresh = i
                break
        
        #lowThresh and maxThresh can be replaces with two numbers where lowThresh =< maxThresh =< 255.  The current values variate from picture to picture
        edges = cv2.Canny(gray,lowThresh,maxThresh)
        
        #Goes through every pixel on the image assigns it a colour based upon the intensity of the edge map and colour map
        for x in range(len(edges)):
            for y in range(len(edges[0])):
                colour[x][y] = colour[x][y] * (edges[x][y] / 255)
        
        #the below ca be uncommented if you want to see each image as it is complete
        #cv2.imshow("ogImg", ogImg)
        #cv2.imshow("Edges", edges)
        #cv2.imshow("Colour", colour)
        #cv2.waitKey(0)
        
        #Writes the code to file
        cv2.imwrite(imgSave, colour)
        
        #prints how long the process took
        print('Operation time:', round(time.time() - startTime, 2), 'secs')
        
    except Exception as e:
        
        #prints what the error was and which image failed, also tracks it
        print("error was:", e)
        print("Failed to edit:", imgLoc)
        print("Item Number:", i)
        print('Operation time:', round(time.time() - startTime,2), 'secs')
        errorRep.append([i, imgLoc, e, round(time.time() - startTime,2)])

print("--------------------------------------")
print("Errors")

#prints any errors that happened
for [pos, imgLoc, errCode, timeTaken] in errorRep:
    print('Image #:', pos, 'Located at:', imgLoc)
    print('Error was:', errCode)
    print('Time taken for process', timeTaken)

print("--------------------------------------")
print('Completed')