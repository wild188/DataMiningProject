import numpy as np
from collections import namedtuple
import sys
from operator import itemgetter

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
    print "Con user len: ", len(conUserInfo)
    index = np.searchsorted(userInfo[:,0], transaction[0])
    print "Found user: ", transaction[0],"=", conUserInfo[index][0][0], " at index: ", index

    transaction = np.array(transaction, dtype='i8')

    #adding item_id to list
    try:
        conUserInfo[index][1].append(transaction[1])
    except IndexError:
        #print conUserInfo[index]
        conUserInfo[index] = [conUserInfo[index], [], [], [], []]
        conUserInfo[index][1] = conUserInfo[index][1] + [transaction[1]]
        #print "Balls", conUserInfo[index]

    #adding category_id to list
    try:
        conUserInfo[index][2] = conUserInfo[index][2] + [transaction[2]]
    except IndexError:
        conUserInfo[index].append([transaction[2]])
        #print conUserInfo[index]

    #add merchant_id to list
    try:
        conUserInfo[index][3] = conUserInfo[index][3] + [transaction[3]]
    except IndexError:
        conUserInfo[index].append([transaction[3]])

    #add brand_id to list
    try:
        conUserInfo[index][4].append(transaction[4])
    except IndexError:
        conUserInfo[index].append([transaction[3]])

    print conUserInfo[index]
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
print userInfo
userInfo = np.asarray(userInfo, dtype='i8')
#userInfo = userInfo.ravel().view([('userid','i4'),('age','i4'),('gender', 'i4'),]) #.astype([('userid','i4'),('age','i4'),('gender', 'i4'),])
sorted(userInfo, key=itemgetter(0))
print userInfo
print userInfo[1]
userInfo = userInfo.tolist()
print userInfo[0]

#billy = np.array([])
#billy = np.hstack((userInfo[:1], userInfo[1:2], userInfo[2:]))
#print billy

#userInfo.sort(axis=0)#, order= 'userid')

userInfo = sorted(userInfo, key=itemgetter(0))

conUserInfo = []#[[[-1]]] * 200 # len(userInfo)
#np.repeat(conUserInfo, userInfo.size, axis=0)
3
#userInfo = userInfo['userid']
#print userInfo
i = 0
total = len(userInfo)
print 100000, userInfo[100000][0]
#print userInfo['userid']
print len(userInfo)
while i in range(len(userInfo)):
    #print i, userInfo[i]
    #print "Original: ", i, userInfo[i]
    #printProgress(i, total)
    #conUserInfo = np.append(conUserInfo, [[row[0]], [row[1]], [row[2]], [], [], [], []])
    #print conUserInfo
    #print conUserInfo[i][0]

    conUserInfo.append([])
    conUserInfo[i].append(userInfo[i])
    conUserInfo[i].append([])
    conUserInfo[i].append([])
    conUserInfo[i].append([])
    conUserInfo[i].append([])

    
    i += 1
    #conUserInfo[i][0] = [userInfo[i][0], userInfo[i][1], userInfo[i][2]]
    #print "Copied: ", i, conUserInfo[i]
    printProgress(i, total)
    #conUserInfo[i][0][0] = row[0]
    #conUserInfo[i][0][0] = row[1]
    #conUserInfo[i][0][0] = row[2]
    #try:
     #   print (i-1), conUserInfo[i-1]
      #  i += 1
    #except IndexError:
     #   print "Balls"
      #  i += 1
        
#print conUserInfo

userInfo = np.array(userInfo)
print userInfo
print len(conUserInfo)
print conUserInfo[90]
print i

i = 0
for i in range(100):
    print conUserInfo[i+10]
    i +=1

consolidate()
conUserInfo = np.array(conUserInfo)
print conUserInfo
#saveResults()