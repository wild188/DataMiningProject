import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from operator import itemgetter
import csv

def makeSubFile():
    global results

    testingTargets = np.load("datasets/test_data.npy")
    print "Read in testing information"

    f=open("datasets/mySubmit", "w+")
    for i in range(len(testingTargets)):
        f.write("%d#%d, #d", testingTargets[i][0], testingTargets[i][1], results[i])
        i+= 1
    f.close()

def prepareData():
    global trainingData
    global testingData
    global trainingResults

    trainingData = np.load("datasets/trainingData.npy")
    print trainingData

    testingData = np.load("datasets/testingData.npy")
    print testingData

    t = len(trainingData[0]) - 1
    trainingResults = map(itemgetter(t), trainingData)
    trainingResults = np.array(trainingResults)
    print trainingResults

    trainingData = trainingData.tolist()
    trainingData = trainingData[:, t-1]
    trainingData = np.array(trainingData)

def testMod():
    global trainingData
    global testingData
    global trainingResults

    X_train, X_test, y_train, y_test = train_test_split(trainingData, trainingResults, test_size=0.4, random_state=0)

    clf1 = LogisticRegression(random_state=1).fit(X_train, y_train)
    clf2 = RandomForestClassifier(random_state=1).fit(X_train, y_train)
    clf3 = GaussianNB().fit(X_train, y_train)

    print clf1.score(X_test, y_test)
    print clf1.score(X_test, y_test)
    print clf1.score(X_test, y_test)

    eclf = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='hard')

    for clf, label in zip([clf1, clf2, clf3, eclf], ['Logistic Regression', 'Random Forest', 'naive Bayes', 'Ensemble']):
    	scores = cross_val_score(clf, trainingData, trainingResults, cv=5, scoring='accuracy')
    	print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))

results= []
prepareData()
print "Prepared all data"
testMod()
print "Tested"