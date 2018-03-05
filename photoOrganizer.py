import os
import time
import datetime
import platform
from PIL import Image
from os import walk

def getPathFromUser():
    pathToOrganize = ""
    while True:
        if pathToOrganize == 'q':
            quit()
        elif os.path.isdir(pathToOrganize):
            break
        else:
            print("Enter Path Directory to Organize (q to quit)")
            pathToOrganize = input()
            pathToOrganize = pathToOrganize.replace(" ", "")
        return pathToOrganize

def creationMonthYearOfFile(filename, timeUnitToReturn):
    if platform.system() == 'Windows':
        dateObject = datetime.datetime.strptime(time.ctime(os.path.getctime(filename)), "%a %b %d %H:%M:%S %Y")
    else:
        try:
            dateObject = datetime.datetime.strptime(time.ctime(os.stat(filename).st_birthtime), "%a %b %d %H:%M:%S %Y")
        except AttibuteError:
            dateObject = datetime.datetime.strptime(time.ctime(os.stat(filename).st_mtime), "%a %b %d %H:%M:%S %Y")
    if timeUnitToReturn == "month":
        return dateObject.strftime("%B")
    elif timeUnitToReturn == "year":
        return dateObject.strftime("%Y")
    else:
        return dateObject.strftime("%B %Y")

def originalMonthYearOfImage(filename, timeUnitToReturn):
    date = Image.open(filename)._getexif()[36867]
    date = datetime.datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    if timeUnitToReturn == "month":
        return date.strftime("%B")
    elif timeUnitToReturn == "year":
        return date.strftime("%Y")
    else:
        return date.strftime("%B %Y")

def organizeFolder(pathToOrganize):
    t0 = time.time()
    os.chdir(pathToOrganize)

    files = []
    for (dirpath, dirnames, filenames) in walk(pathToOrganize):
        files.extend(filenames)
        break

    for someFile in files:

        if os.path.isdir(someFile) or someFile[0]==".":
            continue
        try:
            creationYear = originalMonthYearOfImage(someFile, "year")
            creationMonth = originalMonthYearOfImage(someFile, "month")
        except:
            creationYear = creationMonthYearOfFile(someFile, "year")
            creationMonth = creationMonthYearOfFile(someFile, "month")

        if someFile[-4:] != ".jpg" and someFile[-4:] != ".jp2" and someFile[-4:] != ".png" and someFile[-5:] != ".tiff" and someFile[-4:] != ".bmp" and someFile[-4:] != ".gif" and someFile[-4:] != ".exr" and someFile[-4:] != ".pdf":
            if not os.path.isdir("Non Photos"):
                os.mkdir("Non Photos")
            os.rename(someFile, "Non Photos/"+someFile)
        elif creationYear and creationMonth:
            if not os.path.isdir(creationYear):
                os.mkdir(creationYear)
                os.mkdir(creationYear+'/'+creationMonth)
            elif not os.path.isdir(creationYear+'/'+creationMonth):
                os.mkdir(creationYear+'/'+creationMonth)
            os.rename(someFile, creationYear+'/'+creationMonth+'/'+someFile)
        else:
            if not os.path.isdir("Not Dated"):
                os.mkdir("Not Dated")
            os.rename(someFile, "Not Dated/"+someFile)
            continue

    print("Done Organizing " + pathToOrganize)

    t1 = time.time()
    totalTime = t1 - t0
    print(f"It took {totalTime:.2f} seconds to organize")

# pathToOrganize = getPathFromUser()
pathToOrganize = "/Users/erikfisher/Desktop/test"


organizeFolder(pathToOrganize)
