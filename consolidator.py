import numpy as np
from collections import namedtuple
import sys
from operator import itemgetter
import bisect

UserStruct = namedtuple("MyStruct", "userID age gender items cats merchants brands")

def findex(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        #print("\n\n\n FOUND!!! \n\n\n")
        return i
    
    return -1

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
    global conUserInfo

    userInfo = np.load("datasets/userLog.npy")
    userInfo = np.delete(userInfo, (0), axis=0)
    print("Read in user information")
    purchaseInfo = np.load("datasets/purchase_info.npy")
    purchaseInfo = np.delete(purchaseInfo, (0), axis=0)
    print("Read in purchase information")
    conUserInfo = np.load("datasets/UserInfo2.npy")
    print("Read in user information 2")

def addIfMissing(array, value):
    try:
        array.index(value)
    except ValueError:
        array.append(value)


def updateUserInfo(transaction):
    global userInfo
    global conUserInfo
    global userLookup
    global errorNum
    global transNum

    #print "Con user len: ", len(conUserInfo)
    #index = np.searchsorted(userInfo[:,0], transaction[0])
    transaction = np.array(transaction, dtype='i8')
    index = findex(userLookup, transaction[0])
    if index < 0:
        print "At index: ", index, "We Did not find ", userInfo[index], " = ", transaction[0], " and wrote to ", conUserInfo[index]
        print transaction
        print "ERROR!!!"
        errorNum += 1
        print errorNum

        f=open("error_log.txt", "a+")
        f.write("Error updating for transaction# %d" %transNum)
        f.close()
        return

    #print "Found user: ", transaction[0],"=", conUserInfo[index][0][0], " at index: ", index

    #transaction = np.array(transaction, dtype='i8')
    #print "At index: ", index, "We found ", userInfo[index], " = ", transaction[0], " and wrote to ", conUserInfo[index]
    #print transaction
    #adding item_id to list
    addIfMissing(conUserInfo[index][1], transaction[1])
#    try:
#        conUserInfo[index][1].append(transaction[1])
#    except IndexError:
        #print conUserInfo[index]
#        conUserInfo[index] = [conUserInfo[index], [], [], [], []]
#        conUserInfo[index][1] = conUserInfo[index][1] + [transaction[1]]
        #print "Balls", conUserInfo[index]

    #adding category_id to list
    addIfMissing(conUserInfo[index][2], transaction[2])
#    try:
#        conUserInfo[index][2] = conUserInfo[index][2] + [transaction[2]]
#    except IndexError:
#        conUserInfo[index].append([transaction[2]])
 #       #print conUserInfo[index]
#
 #   #add merchant_id to list
    addIfMissing(conUserInfo[index][3], transaction[3])
  #  try:
   #     conUserInfo[index][3] = conUserInfo[index][3] + [transaction[3]]
    #except IndexError:
     #   conUserInfo[index].append([transaction[3]])
#
    #add brand_id to list
    addIfMissing(conUserInfo[index][4], transaction[4])
 #   try:
  #      conUserInfo[index][4].append(transaction[4])
   # except IndexError:
    #    conUserInfo[index].append([transaction[4]])
#
    #print conUserInfo[index]

def updateMerchantInfo(transaction):
    global conMerchantInfo
    global merchantLookup
    transaction = np.array(transaction, dtype='i8')

    index = findex(merchantLookup, transaction[3])
    if index < 0:
        conMerchantInfo.append([])
        index = len(conMerchantInfo) - 1
        merchantLookup.append(transaction[3])
        conMerchantInfo[index].append([])
        conMerchantInfo[index].append([])
        conMerchantInfo[index].append([])
        conMerchantInfo[index].append([])
        conMerchantInfo[index].append([])
        conMerchantInfo[index].append([])
        conMerchantInfo[index][0].append(transaction[3])

    addIfMissing(conMerchantInfo[index][1], transaction[1])
    addIfMissing(conMerchantInfo[index][2], transaction[2])
    addIfMissing(conMerchantInfo[index][3], transaction[3])
    addIfMissing(conMerchantInfo[index][4], transaction[4])       

    merchantLookup = sorted(merchantLookup)
    conMerchantInfo = sorted(conMerchantInfo, key=itemgetter(0))

def interpretTransaction(transaction):
    updateUserInfo(transaction)
    updateMerchantInfo(transaction)
    
def consolidate():
    global userInfo
    global purchaseInfo
    global conUserInfo
    global transNum

    total = len(purchaseInfo)
    transNum = 0
    for row in purchaseInfo:
        interpretTransaction(row)
        if (transNum % 1000) == 0:
            printProgress(transNum, total, "Processing Transactions")
        transNum += 1

def saveResults():
    global conUserInfo
    global conMerchantInfo
    print("Saving results")
    conUserInfo = np.array(conUserInfo)
    conMerchantInfo = np.array(conMerchantInfo)

    with open("datasets/consUserInfo.npy", 'w') as f:
    	np.save(f, conUserInfo);
    print("Saved user information")

    with open("datasets/consMerchInfo.npy", 'w') as f:
    	np.save(f, conMerchantInfo);
    print("Saved merchant information")

userInfo = np.array([])
purchaseInfo = np.array([])
merchantLookup = []
transNum = 0
errorNum = 0
#conUserInfo = np.array([UserStruct(0, 0, 0, np.array([]), np.array([]), np.array([]), np.array([]))], dtype=object)
conMerchantInfo = []
conUserInfo = []

f=open("errpr_log.txt", "a+")
f.write("Error updating for transaction# %d" %transNum)
f.close()


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
print findex(userInfo, userInfo[100])

i = 0
total = len(userInfo)
print 100000, userInfo[100000][0]
print len(userInfo)
print userInfo[12062]

userInfo = np.array(userInfo)
print userInfo
print len(conUserInfo)
print conUserInfo[90]
print i

i = 0
for i in range(100):
    print conUserInfo[i+10]
    i +=1
conUserInfo = np.array(conUserInfo)
#with open("datasets/UserInfo2.npy", 'w') as f:
#    np.save(f, conUserInfo);
#    print("Saved user information")

conUserInfo = conUserInfo.tolist()
userLookup = userInfo[:,0]
print userLookup

consolidate()
conUserInfo = np.array(conUserInfo)
print conUserInfo
saveResults()
print "Saved results"
print "Total errors: ", errorNum