import os

#Target for the removal of possible duplicates.  Don't run in the original file this will delete all the main files
TARGET = 'D:\\Pictures\\BackgroundOut\\'

if TARGET[-1] == "\\":
    #Cycle through the folder deleting files that don't end with 'Outlines'.
    for entry in os.scandir(TARGET):
        end = entry.path.split('.')
        if not end[0].endswith('Outline'):
            os.remove(entry.path)