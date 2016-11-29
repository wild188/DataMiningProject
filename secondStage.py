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

    with open("datasets/user_info.csv", 'rb') as f:
	reader = csv.reader(f)
	userInfo = list(reader);
    print("Read in user information.");

    with open("datasets/user_log.csv", 'rb') as f:
	reader = csv.reader(f)
	purchaseInfo = list(reader);
    print("Read in purchase information.")

def writePreproccessData():
    with open('names.csv', 'w') as csvfile:
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
        writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

#initialize data arrays
trainData = [];
trainResults = [];
userInfo = []
purchaseInfo = []

#read in data into memory
#readInData();
writePreproccessData()
print("Read in all Data.");


print(trainData[1]);
print(trainResults[1]);
print(userInfo[1]);
print(purchaseInfo[100000]);