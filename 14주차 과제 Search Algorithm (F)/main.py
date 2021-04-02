import numpy as np

def main():
    ml = ML()
    fileName = input("Enter the file name of training data: ")
    ml.setData('train', fileName)
    fileName = input("Enter the file name of test data: ")
    ml.setData('test', fileName)
    ml.buildModel()
    ml.testModel()
    ml.report()

class ML:
    def __init__(self):
        self._trainDX = np.array([]) # Feature value matrix (training data)
        self._trainDy = np.array([]) # Target column (training data)
        self._testDX = np.array([])  # Feature value matrix (test data)
        self._testDy = np.array([])  # Target column (test data)
        self._testPy = np.array([])  # Predicted values for test data
        self._rmse= 0          # Root mean squared error
        self._aType = 0        # Type of learning algoritm
        self._w = np.array([]) # Optimal weights for linear regression
        self._k = 0            # k value for k-NN

    def setData(self, dtype, fileName): # set class variables
        XArray, yArray = self.createMatrices(fileName)
        if dtype == 'train':
            self._trainDX = XArray
            self._trainDy = yArray
        elif dtype == 'test':
            self._testDX = XArray
            self._testDy = yArray
            self._testPy = np.zeros(np.size(yArray)) # Initialize to all 0
            
    def createMatrices(self, fileName): # Read data from file and make arrays
        infile = open(fileName, 'r')
        XSet = []
        ySet = []
        for line in infile:
            data = [float(x) for x in line.split(',')]  # line마다 ,를 분할해 각각의 데이터 x에 대해 실수화한다.
            features = data[0:-1]
            target = data[-1]   # 마지막 열만 target이 된다.
            XSet.append(features)
            ySet.append(target)
        infile.close()
        XArray = np.array(XSet)   # 각 입력된 데이터가 각 행에 입력된다.
        yArray = np.array(ySet)
        return XArray, yArray

    def buildModel(self):
        print()
        print("Which learning algorithm do you want to use?")
        print(" 1. Linear Regression")
        print(" 2. k-NN")
        aType = int(input("Enter the number: "))
        self._aType = aType
        if aType == 1:
            self._w = self.linearRegression()
        elif aType == 2:
            self._k = int(input("Enter the value for k: "))

    def linearRegression(self): # Do linear regression and return optimal w
        X = self._trainDX
        n = np.size(self._trainDy)
        X0 = np.ones([n, 1])
        nX = np.hstack((X0, X)) # Add a column of all 1's as the first column. 절편이 추가되어 열이 한 개 추가.
        y = self._trainDy
        t_nX = np.transpose(nX)
        return np.dot(np.dot(np.linalg.inv(np.dot(t_nX, nX)), t_nX), y)

    def testModel(self):
        n = np.size(self._testDy)
        if self._aType == 1:
            self.testLR(n)
        elif self._aType == 2:
            self.testKNN(n)

    def testLR(self, n): # Test linear regression with the test set
        for i in range(n):
            self._testPy[i] = self.LR(self._testDX[i])
 
    def LR(self, data): # Apply linear regression to a test data
        nData = np.insert(data, 0, 1)
        return np.inner(self._w, nData)
        
    def testKNN(self, n): # Apply k-NN to the test set
        for i in range(n):
            self._testPy[i] = self.kNN(self._testDX[i])

    ### Implement the following and other necessary methods
    def kNN(self, query):
        k = self._k   # 가장 인접한 이웃의 갯수
        All = []   # 각 거리와 인덱스를 저장할 리스트
        for i in range(len(self._trainDX)):   # 모든 train 데이터에 대하여 계산
            trainData = self._trainDX[i]   # i번째 train 데이터
            n = np.size(trainData)   # 각 데이터의 좌표 갯수
            dis = 0
            for j in range(n):
                dis += (query[j] - trainData[j])**2  # 각 원소의 차이에 제곱
            distanceAndIndex = [dis, i]
            All.append(distanceAndIndex)
        All.sort()
        NN = All[0:k]
        NN = np.array(NN)
        index = NN[:,1]
        total = 0
        for i in index:
            total += self._trainDy[int(i)]
        return total/k

    def report(self):
        self.calcRMSE()
        print()
        print("RMSE: ", round(self._rmse, 2))

    def calcRMSE(self):
        n = np.size(self._testDy) # Number of test data
        totalSe = 0
        for i in range(n):
            se = (self._testDy[i] - self._testPy[i]) ** 2
            totalSe += se
        self._rmse = np.sqrt(totalSe) / n


main()
