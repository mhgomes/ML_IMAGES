import os
import re
import random

path = "darknetConverted"
if not os.path.exists(path):
    os.makedirs(path)
path = "temp"
if not os.path.exists(path):
    os.makedirs(path)
for root, dirs, files in os.walk("ann"):
    classList = []
    numFiles = 0
    for filename in files:
        numFiles += 1
        oldFile = open("ann/"+filename)
        ending = ".png.json"
        filename = filename[:-len(ending)]
        #filename = filename[:len(filename)-10]
        newFile = open("darknetConverted/"+filename+".txt", "w+")
        for line in oldFile:
            takeNextWord = False
            words = line.split()
            #print(words)
            n = 0
            for word in words:
                classType = -1
                if takeNextWord:
                    xList = []
                    yList = []
                    i = 0
                    for string in classList:
                        if word == classList[i]:
                            classType = i
                        if classType != -1:
                            break
                        i = i+1
                    #print(i)
                    points = []
                    #print(word)
                    #print(word[1:len(word)-2])
                    if i > len(classList)-1:
                        print("len = "+str(len(classList)))
                        print("\nclassType = "+str(classType))
                        classList.append(word)
                        print("\nAppending "+word)
                    #classList[i]=word[1:len(word)-3]
                    g=n
                    while "]]" not in words[g]:
                        if "[[" in words[g]:
                            x = re.search("[[][[](.*),",words[g]).group(1)
                            xList.append(float(x))
                            print("X, "+x)
                        elif "]" in words[g]:
                            y =words[g][:len(words[g])-2]
                            yList.append(float(y))
                            print("Y, "+y)
                        elif "[" in words[g]:
                            x = re.search("[[](.*),", words[g]).group(1)
                            xList.append(float(x))
                            print("X, "+x)
                        g=g+1
                    y = words[g][:len(words[g])-3]
                    yList.append(float(y))
                    print("Y, "+y)
                    # calculate centroid
                    center = (max(xList) + min(xList)) / 2.0, (max(yList) + min(yList)) / 2.
                    print("Center x: "+str(center[0]))
                    print("Center y: "+str(center[1]))
                    maxX = max(xList)
                    minX = min(xList)
                    maxY = max(yList)
                    minY = min(yList)
                    width = maxX-minX
                    height = maxY-minY
                    newFile.write(str(classType)+" "+str(center[0])+" "+str(center[1])+" "+str(width)+" "+str(height)+"\n")
                n=n+1
                if word == "\"classTitle\":":
                    if takeNextWord:
                        takeNextWord=False
                    else:
                        takeNextWord=True
                else:
                    takeNextWord=False
    objFile = open("obj.names","w+")
    for string in classList:
        objFile.write(string[1:len(string)-2]+"\n")
    objData = open("obj.data", "w+")
    objData.write("classes = "+str(len(classList))+"\ntrain = data/train.txt\nvalid = data/test.txt\nnames = data/obj.names\nbackup = backup/")
train = open("train.txt", "w+")
val = open("test.txt", "w+")
for i in range(0, int(numFiles/6)):
    filename = random.choice(os.listdir("img"))
    os.rename("img/"+filename, "temp/"+filename)
    val.write(filename+"\n")
for root, dirs, files in os.walk("img"):
    for filename in files:
        train.write(filename+"\n")
for root, dirs, files in os.walk("temp"):
    for filename in files:
        os.rename("temp/" + filename, "img/" + filename)
os.rmdir(path)
