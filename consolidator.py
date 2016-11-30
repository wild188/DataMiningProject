import numpy as np
from collections import namedtuple
UserStruct = namedtuple("MyStruct", "userID age gender items cats merchants brands")

def readData():
    global userInfo
    global purchaseInfo 

    userInfo = np.load("datasets/userLog.npy")
    userInfo = np.delete(userInfo, (0), axis=0)
    print("Read in user information")
    #purchaseInfo = np.load("datasets/purchase_info.npy")
    #purchaseInfo = np.delete(purchaseInfo, (0), axis=0)
    #print("Read in purchase information")

def updateUserInfo(transaction):
    global userInfo
    global conUserInfo
    print conUserInfo
    index = np.searchsorted(userInfo[:,0], transaction[0])
    #adding item_id to list
    conUserInfo[index][3] = np.append(conUserInfo[index][3], transaction[1])

    #adding category_id to list
    conUserInfo[index][4] = np.append(conUserInfo[index][2],transaction[2])

    #add merchant_id to list
    conUserInfo[index][5] = np.append(conUserInfo[index][3], transaction[3])
    
    #add brand_id to list
    conUserInfo[index][6] = np.append(conUserInfo[index][6], transaction[4])

    #adding item_id to list
    #conUserInfo[index].items = np.append(conUserInfo[index].items, transaction[1])
    #adding category_id to list
    #conUserInfo[index].cats = np.append(conUserInfo[index].cats,transaction[2])
    #add merchant_id to list
    #conUserInfo[index].merchants = np.append(conUserInfo[index].merchants, transaction[3])
    #add action to list

def updateMerchantInfo(transaction):
    global conMerchantInfo
    global merchantLookup

def interpretTransaction(transaction):
    updateUserInfo(transaction)
    updateMerchantInfo(transaction)
    
def consolidate():
    global userInfo
    global purchaseInfo
    global conUserInfo

    
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


#conUserInfo = np.array([UserStruct(0, 0, 0, np.array([]), np.array([]), np.array([]), np.array([]))], dtype=object)
conMerchantInfo = np.array([])
readData()

userInfo = np.array(userInfo)
userInfo.sort(axis=0)
conUserInfo = np.array([([[0], [0], [0], [], [], [], []]) * 1000])
#np.repeat(conUserInfo, userInfo.size, axis=0)
i = 0
print userInfo.size
for row in userInfo:
    #print row
    np.append(conUserInfo, [[row[0]], [row[1]], [row[2]], [], [], [], []])
    #print conUserInfo
    #print conUserInfo[i][0]
    #conUserInfo[i][0][0] = row[0]
    #conUserInfo[i][0][0] = row[1]
    #conUserInfo[i][0][0] = row[2]
    i += 1

print conUserInfo.size
print i

consolidate()
saveResults()