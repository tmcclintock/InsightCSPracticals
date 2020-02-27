import numpy as np

class Regressor(object):
    def __init__(self, X, y, with_bias = True,
                 test_percent = 0.3, normed = False):
        self.with_bias = with_bias
        self.test_percent = test_percent
        self.normed = normed

        self.set_Xy(X, y)

        self.computed = False

        self.compute()

    def set_Xy(self, X, y, ):
        if len(np.shape(X)) == 1:
            self.N = len(X)
            self.M = 1
            X = np.atleast_2d(X).T
        else:
            self.N = len(X) #number of data points
            self.M = len(X[0]) #number of features
        self.X = X

        self.Ntrain = int((1-self.test_percent) * self.N)
        self.Ntest = self.N - self.Ntrain

        inds = np.arange(self.N)
        traininds = np.random.choice(inds, size=self.Ntrain, replace = False)
        self.Xtrain = X[traininds]
        self.ytrain = y[traininds]
        
        testinds = []
        for i in inds:
            if i in traininds:
                continue
            else:
                testinds.append(i)
        testinds = np.array(testinds)
        self.Xtest = X[testinds]
        self.ytest = y[testinds]

        self.computed = False
        return
        
    def compute(self):
        self.computed = True
        
        if self.with_bias:
            O = np.ones(self.Ntrain).reshape(self.Ntrain, 1)
            X = np.hstack((O, self.Xtrain))
        else:
            X = self.Xtrain

        XX = np.dot(X.T, X)
        XY = np.dot(X.T, self.ytrain)
        self.parameters = np.linalg.solve(XX, XY)
        self.param_cov = XX
        self.param_unc = XX.diagonal()
        return

    def predict(self, x):
        if len(x) == self.M:
            print("here")
            if self.with_bias:
                x = np.concatenate(([1], x))
            return np.dot(x, self.parameters)
        elif len(x[0]) == self.M:
            if self.with_bias:
                x = np.hstack((np.ones(len(x)).reshape(len(x),1), x))
            return np.dot(x, self.parameters)

    def chi2(self, y, y_est):
        y = np.asarray(y)
        y_est = np.asarray(y_est)
        var = np.var(y)
        return np.sum((y - y_est)**2/var)

    def correlation(self, X, y):
        X = np.squeeze(X)
        y = np.squeeze(y)
        assert len(np.shape(X)) == 1
        assert len(np.shape(y)) == 1
        cov = np.cov(X, y)
        return cov[0,1]/np.sqrt(cov[0,0]*cov[1,1])
        
if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv("USA_Housing.csv")
    y = data.Price
    X = data["Avg. Area Number of Rooms"]

    model = Regressor(X, y)
    Xtest, ytest = model.Xtest, model.ytest
    y_est = model.predict(Xtest)
