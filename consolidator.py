import numpy as np
from collections import namedtuple
import sys
UserStruct = namedtuple("MyStruct", "userID age gender items cats merchants brands")

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

def readData():
    global userInfo
    global purchaseInfo 

    userInfo = np.load("datasets/userLog.npy")
    userInfo = np.delete(userInfo, (0), axis=0)
    print("Read in user information")
    purchaseInfo = np.load("datasets/purchase_info.npy")
    purchaseInfo = np.delete(purchaseInfo, (0), axis=0)
    print("Read in purchase information")

def updateUserInfo(transaction):
    global userInfo
    global conUserInfo
    print conUserInfo.size
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
total = 200000
print userInfo.size
for row in userInfo:
    #print row
    printProgress(i, total)
    conUserInfo = np.append(conUserInfo, [[row[0]], [row[1]], [row[2]], [], [], [], []])
    #print conUserInfo
    #print conUserInfo[i][0]
    #conUserInfo[i][0][0] = row[0]
    #conUserInfo[i][0][0] = row[1]
    #conUserInfo[i][0][0] = row[2]
    i += 1

print conUserInfo.size
print conUserInfo[1000]
print i

consolidate()
saveResults()