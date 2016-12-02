### Billy DeLucia ###

#Imported Modules
import csv
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

    #with open("datasets/user_log.csv", 'rb') as f:
	#reader = csv.reader(f)
	#purchaseInfo = list(reader);
    #print("Read in purchase information.")

def writePreproccessTrainingData():
    with open('datasets/PreTrain.csv', 'w') as csvfile:
        fieldnames = ['user_id#merchant_id', 'user_id', 'merchant_id', 'age_range', 'gender']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        count = 0
        total = 130365
        for row in trainResults:
            if count == 0:
                count += 1
                continue
            count += 1
            userIndex = [i for i, x in enumerate(userInfo) if x[0] == row[0]][0]
            #print(userIndex, row[0], userInfo[106340])
            writer.writerow({'user_id#merchant_id' : str(row[0])+"#"+str(row[1]), 'user_id' : row[0],'merchant_id' : row[1],
            'age_range' : userInfo[userIndex][1], 'gender' : userInfo[userIndex][2]})
            printProgress(count, total)

#initialize data arrays
#global trainData = [];
#global trainResults = [];
#global userInfo = []
#global purchaseInfo = []

#read in data into memory
readInData();
#print(userInfo)
writePreproccessTrainingData()
print("Read in all Data.");


#print(trainData[1]);
print(trainResults[1]);
#print(userInfo[1]);
#print(purchaseInfo[100000]);