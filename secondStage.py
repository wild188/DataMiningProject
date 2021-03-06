### Billy DeLucia ###

#Imported Modules
import csv

def readInData():
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

    #with open("datasets/user_info.csv", 'rb') as f:
	#reader = csv.reader(f)
	#userInfo = list(reader);
    #print("Read in user information.");

    #with open("datasets/user_log.csv", 'rb') as f:
	#reader = csv.reader(f)
	#purchaseInfo = list(reader);
    #print("Read in purchase information.")

def writePreproccessTrainingData():
    with open('datasets/PreTrain.csv', 'w') as csvfile:
        fieldnames = ['user_id#merchant_id', 'user_id', 'merchant_id' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in trainResults:
            writer.writerow({'user_id#merchant_id' : str(row[0])+"#"+str(row[1]), 'user_id' : row[0], 'merchant_id' : row[1]})

#initialize data arrays
trainData = [];
trainResults = [];
userInfo = []
purchaseInfo = []

#read in data into memory
readInData();
writePreproccessTrainingData()
print("Read in all Data.");


#print(trainData[1]);
print(trainResults[1]);
#print(userInfo[1]);
#print(purchaseInfo[100000]);