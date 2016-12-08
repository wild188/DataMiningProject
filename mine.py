import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import log_loss
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
import sklearn.linear_model
import sklearn.calibration
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from operator import itemgetter
import csv

def makeSubFile():
    global results

    testingTargets = np.load("datasets/test_data.npy")
    print "Read in testing information"

    f=open("datasets/mySubmit_all_Just_CalClass_with_avging.csv", "w+")
    f.write("user_id#merchant_id,prob\n")
    for i in range(len(testingTargets)):
        f.write("%s#%s,%s\n" %(testingTargets[i][0], testingTargets[i][1], results[i][1]))
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
    print range(t)
    trainingResults = map(itemgetter(t), trainingData)
    trainingResults = np.array(trainingResults)
    print trainingResults

    #trainingData = trainingData.tolist()
    trainingData = map(itemgetter(range(t)), trainingData)#trainingData[t:, 1]
    trainingData = np.array(trainingData)
    print trainingData

def testMod():
    global trainingData
    global testingData
    global trainingResults

    X_train, X_test, y_train, y_test = train_test_split(trainingData, trainingResults, test_size=0.4, random_state=0)
    p = LogisticRegressionCV(scoring='neg_log_loss', random_state=1, n_jobs = -1)
    clf1 = sklearn.calibration.CalibratedClassifierCV()#.fit(X_train, y_train)
    clf2 = sklearn.ensemble.RandomForestClassifier()#.fit(X_train, y_train)
    clf3 = sklearn.ensemble.ExtraTreesClassifier()#.fit(trainingData, trainingResults) #SGDClassifier(loss='log', fit_intercept= False).fit(X_train, y_train)

    #print clf2.feature_importances_

    print X_train, X_test, y_train, y_test

    #print clf1.score(X_test, y_test)
    #print clf1.score(X_test, y_test)
    #print clf1.score(X_test, y_test)

    #print "RFC weights: ", clf2.feature_importances_

    eclf = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='soft', weights=[1, 1, 1])

    #for clf, label in zip([clf1, clf2, clf3, eclf], ['Logistic Regression', 'Random Forest', 'extra tree reg', 'Ensemble']):
    scores = cross_val_score(clf1, trainingData, trainingResults, cv=5, scoring='neg_log_loss')
    print("Accuracy: %0.5f (+/- %0.5f) [%s]" % (scores.mean(), scores.std(), label))

def popResults():
    global results
    global trainingData
    global testingData
    global trainingResults

    #model = LogisticRegression().fit(trainingData, trainingResults)
    #model = RandomForestClassifier().fit(trainingData, trainingResults)
    #model = GaussianNB().fit(trainingData, trainingResults)
    #pre_model = LogisticRegressionCV(scoring='neg_log_loss', random_state=1, n_jobs = -1)#.fit(trainingData, trainingResults)
    model = sklearn.calibration.CalibratedClassifierCV().fit(trainingData, trainingResults)
    #model = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='soft', weights=[1, 1, 1])
    #eclf.fit(trainingData, trainingResults)
    #model.fit(trainingData, trainingResults)
    print model.predict_proba(testingData)
    results = model.predict_proba(testingData)
    print model.predict(testingData)


results= []
prepareData()
print "Prepared all data"
#testMod()
#print "Tested"

popResults()
print "Calculated results"
makeSubFile()
print "Done"