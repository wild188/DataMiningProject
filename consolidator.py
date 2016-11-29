import numpy as np


def readData():
    global userInfo
    global purchaseInfo 

    userInfo = np.load("datasets/userLog.npy")
    userInfo = np.delete(userInfo, (0), axis=0)
    #print userInfo[:,0]
    #purchaseInfo = np.load("datasets/purchase_info.npy")
    #purchaseInfo = np.delete(purchaseInfo, (0), axis=0)

def updateUserInfo(transaction):
    global userInfo
    global conUserInfo

    index = np.sortedsearch(userInfo[:,0], transaction[0])
    #adding item_id to list
    try:
        conUserInfo[index][3].append(transaction[1])
    except IndexError:
        conUserInfo[index].append([transaction[1]])
    
    #adding category_id to list
    try:
        conUserInfo[index][3].append(transaction[2])
    except IndexError:
        conUserInfo[index].append([transaction[2]])

    #add merchant_id to list
    try:
        conUserInfo[index][3].append(transaction[3])
    except IndexError:
        conUserInfo[index].append([transaction[3]])

    #add action to list
    try:
        conUserInfo[index][4][transaction[4]] += 1
    except IndexError:
        conUserInfo[index].append([0, 0, 0, 0])
        conUserInfo[index][4][transaction[4]] += 1

def updateMerchantInfo(transaction):
    global conMerchantInfo
    global merchantLookup

def interpretTransaction(transaction):
    updateUserInfo(transaction)
    updateMerchantInfo(transaction)
    
def consolidate():
    global userInfo
    global purchaseInfo

    userInfo = np.array(userInfo)
    userInfo.sort(axis=0)
    conUserInfo = userInfo
    print userInfo
    for row in purchaseInfo:
        interpretTransaction(row)

def saveResults():
    with open("datasets/consUserInfo.npy", 'w') as f:
    	np.save(f, conUserInfo);
    print("Saved user information")

    with open("datasets/consMerchInfo.npy", 'w') as f:
    	np.save(f, conMerchantInfo);
    print("Saved merchant information")

userInfo = np.array([])
purchaseInfo = np.array([])
conUserInfo = np.array([])
conMerchantInfo = np.array([])
readData()
consolidate()
saveResults()