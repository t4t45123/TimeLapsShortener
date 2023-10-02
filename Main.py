import os
import cv2
import numpy as np

frames = []
framesToRemove = []
showFrames = True
fps = 0
width = 0
height = 0
totalFrames = 0

def extractFrames(path):
    global fps, width, height, totalFrames  # Make these variables global so we can modify them

    vidcap = cv2.VideoCapture(path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Convert to int
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Convert to int
    totalFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))  # Convert to int
    success, image = vidcap.read()
    count = 0
    success = True

    while success:
        success, image = vidcap.read()
        if success:
            cv2.imwrite("frame%d.jpg" % count, image)
            frames.append("frame%d.jpg" % count)
        count += 1

def mse(img1, img2):
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err / (float(h * w))
    return mse, diff

def getDuplicates():
    global limit
    pf = ""
    ff = ""

    for di in frames:
        if di.endswith("jpg"):
            pf = ff
            ff = di
        if pf != "":
            img1 = cv2.imread(pf)
            img2 = cv2.imread(ff)
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            error, diff = mse(img1, img2)
            #print("Image matching Error between the two images:", error)
            if error > 20 and showFrames:
                #print("Image matching Error between the two images:", error)
                cv2.imshow("diff", diff)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            if error < float(limit):
                framesToRemove.append(ff)

def removeFrames(f):
    global frames
    if f is None:
        count = 0
        dirs = os.listdir(".")
        for di in dirs:
            if di.endswith(".jpg") and di in frames:
                os.remove(di)
                frames.remove(di)
                count += 1
    else:
        for fr in f:
            if fr in frames:
                os.remove(fr)
                frames.remove(fr)
                #print("Removed - " + str(fr))

def framesToVideo():
    global outPath, fps, width, height
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(outPath, fourcc, fps, (width, height))

    for f in frames:
        img = cv2.imread(f)
        out.write(img)
        #print("Added - " + str(f))

    out.release()

path = input("Enter path of existing video: ")
outPath = input("Enter output file name: ")
limit = input("Enter the MSE limit: ")

removeFrames(None)
extractFrames(path)
getDuplicates()
removeFrames(framesToRemove)
framesToVideo()