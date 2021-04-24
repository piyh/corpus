from scipy.spatial import distance
def euc(a,b):
        return distance.euclidean(a,b)

class ScrappyKNN():
    def fit(self,Xtrain, Ytrain):
        self.XTrain = Xtrain
        self.YTrain = Ytrain
        pass
    def predict(self,Xtest):
        predictions = []
        for row in Xtest:
            label = self.closest(row)
            predictions.append(label)
        return predictions
    
    def closest(self,row):
            best_dist = euc(row,self.XTrain[0])
            best_index = 0
            for i in range(1,len(self.XTrain)):
                dist = euc(row, self.XTrain[i])
                if dist < best_dist:
                    best_dist = dist
                    best_index = i
            return self.YTrain[best_index]

from sklearn.datasets import load_iris
iris = (load_iris())
X, Y = (iris.data, iris.target)

from sklearn.cross_validation import train_test_split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,Y, test_size = .5)

clf = ScrappyKNN()
clf.fit(Xtrain, Ytrain)
predictions = clf.predict(Xtest)

from sklearn.metrics import accuracy_score
print(accuracy_score(Ytest, predictions))

#from sklearn import tree
#clf = tree.DecisionTreeClassifier()
#label = random.choice(self.YTrain)
#from sklearn.neighbors import KNeighborsClassifier 
#clf = KNeighborsClassifier()

#print (iris.feature_names)
#print (iris.target_names)
#print (iris.data[0])
#for i in range(len(iris.target)):
#        print ("example{},label {}, features {}".format(i,iris.target[i],iris.data[i]))

#print (test_target)