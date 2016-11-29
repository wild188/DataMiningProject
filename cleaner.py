### Billy DeLucia ###

#Imported Modules
import csv
import numpy as np

def readInData():
    global trainResults
    global userInfo
    global purchaseInfo

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
    

def saveData():
    global trainResults
    global userInfo
    global purchaseInfo

    trainResults = np.asarray(trainResults)
    with open("datasets/train_results.npy", 'w') as f:
    	np.save(f, trainResults);
    print("Saved training results")

    userInfo = np.asarray(userInfo)
    with open("datasets/userLog.npy", 'w') as f:
    	np.save(f, userInfo);
    print("Saved user information")

    purchaseInfo = np.asarray(purchaseInfo)
    with open("datasets/purchase_info.npy", 'w') as f:
    	np.save(f, purchaseInfo);
    print("Saved purchase information")

#read in data into memory
readInData();
saveData()
print("Cleaning complete");