from sklearn import datasets
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
import csv
import numpy as np
import sys
from numpy import genfromtxt

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

def exampleEnsemble ():
	iris = datasets.load_iris()
	X, y = iris.data[:, 1:3], iris.target

	print(iris);

	print(X);
	print(y);

	clf1 = LogisticRegression(random_state=1)
	clf2 = RandomForestClassifier(random_state=1)
	clf3 = GaussianNB()

	eclf = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='hard')

	for clf, label in zip([clf1, clf2, clf3, eclf], ['Logistic Regression', 'Random Forest', 'naive Bayes', 'Ensemble']):
		scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
		print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))	

def addIfMissing(array, value):
    try:
        array.index(value)
    except ValueError:
        array.append(value)


a = []
addIfMissing(a, 1)
addIfMissing(a, 4)
print a
addIfMissing(a, 1)
print a

trainData = [];
trainResults = [];
total = 130365
counter = -1;
with open("datasets/train_label.csv", 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		if(counter < 0):
			counter += 1;
			continue;
		toAdd = row[0].split('#');
		toAdd.append(row[1]);
		trainResults.append(toAdd);
		counter += 1;
print("Read in training data.");

total = 212063;
userInfo = []
counter = -1;
with open("datasets/user_info.csv", 'rb') as f:
	reader = csv.reader(f)
	userInfo = list(reader);
print("Read in user information.");

#userInfo = np.asarray(userInfo)
#with open("datasets/userLog.npy", 'w') as f:
#	np.save(f, userInfo);

user_info2 = np.load("datasets/userLog.npy")
print user_info2
print user_info2[1][1]
#purchaseInfo = []
#total = 26258293
#counter = -1;
#with open("datasets/user_log.csv", 'rb') as f:
#	reader = csv.reader(f)
#	purchaseInfo = list(reader);
#print("Read in purchase information.")