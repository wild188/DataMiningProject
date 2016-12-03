### Billy DeLucia ###

#Imported Modules
import csv
import numpy as np
import sys

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
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

def readInData():
    global trainResults
    global userInfo
    global purchaseInfo
    global testData
    testData = []

    trainResults = []
    with open("datasets/train_label.csv", 'rb') as f:
        reader = csv.reader(f)
        counter = -1;
        for row in reader:
            if(counter < 0):
                counter += 1;
                continue;
            toAdd = row[0].split('#');
            toAdd.append(row[1]);
            trainResults.append(toAdd);
            counter += 1;
    print("Read in training data.");

    with open("datasets/test_label.csv", 'rb') as f:
        reader = csv.reader(f)
        counter = -1;
        for row in reader:
            if(counter < 0):
                counter += 1;
                continue;
            toAdd = row[0].split('#');
            testData.append(toAdd);
            counter += 1;
        print("Read in testing data.");

    userInfo = []
    with open("datasets/user_info.csv", 'rb') as f:
	    reader = csv.reader(f)
	    userInfo = list(reader);
    
    print("Read in user information.");

    with open("datasets/user_log.csv", 'rb') as f:
	    reader = csv.reader(f)
	    purchaseInfo = list(reader);
    print("Read in purchase information.")

#def cleanData():
    
def processUserData():
    global userInfo
    global emptyUserInfoTable
    emptyUserInfoTable = []
    total = len(userInfo)
    i = 0
    while i in range(len(userInfo)):
        emptyUserInfoTable.append([])
        emptyUserInfoTable[i].append(userInfo[i])
        emptyUserInfoTable[i].append([])
        emptyUserInfoTable[i].append([])
        emptyUserInfoTable[i].append([])
        emptyUserInfoTable[i].append([])
        i += 1
        if (i % 1000) == 0:
            printProgress(i, total, "User data table")

def saveData():
    global trainResults
    global userInfo
    global purchaseInfo
    global testData
    global emptyUserInfoTable

    trainResults = np.asarray(trainResults)
    with open("datasets/train_targets.npy", 'w') as f:
    	np.save(f, trainResults);
        print("Saved training results")

    testData = np.array(testData)
    with open("datasets/test_targets.npy", 'w') as f:
    	np.save(f, testData);
        print("Saved testData")

    userInfo = np.asarray(userInfo)
    print userInfo
    with open("datasets/userLog.npy", 'w') as f:
    	np.save(f, userInfo);
        print("Saved user information")

    emptyUserInfoTable = np.array(emptyUserInfoTable)
    with open("datasets/UserInfo2.npy", 'w') as f:
        np.save(f, emptyUserInfoTable);
        print("Saved user information")

    purchaseInfo = np.asarray(purchaseInfo)
    with open("datasets/purchase_info.npy", 'w') as f:
    	np.save(f, purchaseInfo);
        print("Saved purchase information")

#read in data into memory
readInData()
processUserData()
saveData()
print("Cleaning complete");