
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
    testingTargets = np.load("datasets/test_data.npy")
    #purchaseInfo = np.delete(purchaseInfo, (0), axis=0)
    print "Read in testing information"
    userInfo = np.load("datasets/consUserInfo.npy")
    print "Read in user information"
    merchantInfo = np.load("datasets/consMerchInfo.npy")
    print "Read in merchant information"

def genUserLookup():
    global userInfo
    global userLookup
    userLookup = map(itemgetter(0), userInfo)
    #print userLookup
    userLookup = map(itemgetter(0), userLookup)
    #print userLookup

def genMerchantLookup():
    global merchantInfo
    global merchantLookup
    merchantLookup = map(itemgetter(0), merchantInfo)
    merchantLookup = map(itemgetter(0), merchantLookup)

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
        print "User: ", user, "Merchant: ", merchant
        return row
    
    itemScore = simScore(userInfo[userIndex][1], merchantInfo[merchantIndex][1])
    catScore = simScore(userInfo[userIndex][2], merchantInfo[merchantIndex][2])
    merchantScore = lsearch(userInfo[userIndex][3], merchant)
    if merchantScore == -1:
        merchantScore = 0
    else:
        merchantScore = 1

    brandScore = simScore(userInfo[userIndex][4], merchantInfo[merchantIndex][4])

    row.append(userInfo[userIndex][0][1]) #age
    row.append(userInfo[userIndex][0][2]) #gender
    row.append(itemScore)
    row.append(catScore)
    row.append(merchantScore)
    row.append(brandScore)
    
    return row

def genTrainingMatrix():
    global trainingTargets
    global trainingData

    i = 0
    trainingData = []
    total = len(trainingTargets)
    for i in range(total):
        trainingData.append(tupleGen(trainingTargets[i][0], trainingTargets[i][1]))
        trainingData[i].append(trainingTargets[i][2])
        if (i % 1000):
            #print trainingData[i]
            printProgress(i, total, "Training data")
        i += 1
        
def genTestingMatrix():
    global testingTargets
    global testingData

    i = 0
    testingData = []
    total = len(testingTargets)
    for i in range(total):
        toAdd = tupleGen(testingTargets[i][0], testingTargets[i][1])
        if len(toAdd) < 2:
            print "Testing matrix failed"
            return
        testingData.append(toAdd)
        if (i % 1000):
            #print testingData[i]
            printProgress(i, total, "Testing data")
        i += 1

#userLookup = []
#userInfo = []
#merchantInfo = []
#trainingTargets = []
#testingTargets = []
#traingingAnswers = []
readData()
print "Read in Data"
userInfo = userInfo.tolist()

def saveData():
    global trainingData
    global testingData

    trainingData = np.array(trainingData)
    testingData = np.array(testingData)

    with open("datasets/trainingData.npy", 'w') as f:
    	np.save(f, trainingData);
        print("Saved training data")
    
    with open("datasets/testingData.npy", 'w') as f:
    	np.save(f, testingData);
        print("Saved testing data")


trainingTargets = np.array(trainingTargets, dtype='i8')
print "Made training numbers"
print trainingTargets
#testingTargets = np.delete(testingTargets, (0), axis=0)
testingTargets = np.array(testingTargets, dtype='i8')
print "Made testing numbers"
print testingTargets
#trainingTargets = trainingTargets.tolist()
#testingTargets = testingTargets.tolist()
print "Numpy targest are now lists"
genUserLookup()
print "Made user lookup table"
print np.array(userLookup)
genMerchantLookup()
print "Made merchantLookup"
print np.array(merchantLookup)
genTrainingMatrix()
print "Generated training matrix"
genTestingMatrix()
print "Generated testing matrix"
saveData()
print "Saved all data"
