import os

#target for the file that needs fixing
TARGET = 'D:\\Pictures\\Backgrounds\\'


targets = [] #list of all the file inputs

if TARGET[-1] == "\\":
    #Cycle through the folder grabbing any valid pictures 
    for entry in os.scandir(TARGET):
        if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():
            targets.append(entry.path)

j = 0

#cycles through all files and tries to fix the file names
for i, imgLoc in enumerate(targets):
    
    newNam = imgLoc.split('.', 1)
    
    if (newNam[0] + '.' + newNam[1][:3]).endswith('jpg') or (newNam[0] + '.' + newNam[1][:3]).endswith('png'):
        j += 1
        os.rename(imgLoc, newNam[0] + '.' + newNam[1][:2] + 'g')
    else:
        #prints any files that don't seem to be right
        print(imgLoc, newNam[0] + '.' + newNam[1][:2] + 'g')

#return the number of updated files compared the the actual number of files
print(len(targets))
print(j)