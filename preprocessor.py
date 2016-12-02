
import bisect
import sys
from operator import itemgetter

import numpy as np


def findex(array, value):
    """
    Locate the leftmost value exactly equal to the value or -1 if not found
    @params:
        array   - Required  : sorted array
        value   - Required  : target value
    """
    i = bisect.bisect_left(array, value)
    if i != len(array) and array[i] == value:
        #print("\n\n\n FOUND!!! \n\n\n")
        return i
    
    return -1

def lsearch(array, value):
    for i in range(len(array)):
        if(array[i] == value):
            return i
    
    return -1

def simScore(array1, array2):
    score = 0;
    for i in range(len(array1)):
        for j in range(len(array2)):
            if array1[i] == array2[j]:
                score += 1
    return score


def printProgress(iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#'* filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def readData():
    global trainingTargets
    global testingTargets
    global userInfo
    global merchantInfo

    trainingTargets = np.load("datasets/train_results.npy")
    #userInfo = np.delete(userInfo, (0), axis=0)
    print "Read in training information"
    testingTargets = np.load("datasets/purchase_info.npy")
    #purchaseInfo = np.delete(purchaseInfo, (0), axis=0)
    print "Read in testing information"
    userInfo = np.load("datasets/consUserInfo.npy")
    print "Read in user information"
    merchantInfo = np.load("datasets/consMerchInfo.npy")
    print "Read in merchant information"

def genUserLookup():
    global userInfo
    global userLookup
    userLookup = userInfo[:, 0]

def genMerchantLookup():
    global merchantInfo
    global merchantLookup
    merchantLookup = merchantInfo[:, 0]

def tupleGen(user, merchant):
    global userInfo
    global merchantInfo
    global userLookup
    global merchantLookup


    row = []
    userIndex = findex(userLookup, user)
    merchantIndex = findex(merchantLookup, merchant)
    if (userIndex < 0 or merchantIndex < 0):
        print "ERROR: user or merchant not found"
        return row
    
    itemScore = simScore(userInfo[userIndex][1], merchantInfo[merchantIndex][1])
    catScore = simScore(userInfo[userIndex][2], merchantInfo[merchantIndex][2])
    merchantScore = lsearch(userInfo[userIndex][3], merchant)
    if merchantScore == -1:
        merchantScore = 0
    brandScore = simScore(userInfo[userIndex][4], merchantInfo[merchantIndex][4])

    row.append(userInfo[0][1]) #age
    row.append(userInfo[0][2]) #gender
    row.append(itemScore)
    row.append(catScore)
    row.append(merchantScore)
    row.append(brandScore)
    
    return row

def genTrainingMatrix():
    global trainingTargets
    global trainingData

    trainingData = []
    total = len(trainingData)
    for i in range(total):
        trainingData.append(tupleGen(trainingTargets[0], trainingTargets[1]))
        trainingData[i].append(trainingTargets[2])
        if (i % 1000):
            printProgress(i, total, "Generating training data")
        
def genTestingMatrix():
    global testingTargets
    global testingData

    testingData = []
    total = len(testingTargets)
    for i in range(total):
        testingData.append(tupleGen(testingTargets[0], testingTargets[1]))
        if (i % 1000):
            printProgress(i, total, "Generating testing data")

#userLookup = []
#userInfo = []
#merchantInfo = []
#trainingTargets = []
#testingTargets = []
#traingingAnswers = []
readData()
genUserLookup()
print "Made user lookup table"
genMerchantLookup()
print "Made merchantLookup"

print "Read in Data"
genTrainingMatrix()
print "Generated training matrix"
genTestingMatrix()
print "Generated testing matrix"
saveData()
print "Saved all data"
