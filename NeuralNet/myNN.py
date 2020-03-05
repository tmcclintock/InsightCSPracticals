import numpy as np
import scipy.stats as ss

def _sigmoid(z):
    return 1./(1+np.exp(-z))

def _sigmoid_deriv(z):
    sigz = _sigmoid(z)
    return sigz*(1-sigz)

def _softmax(z):
    ez = np.exp(z - np.max(z))
    return ez/np.sum(ez)
    

class DenseLayer(object):
    def __init__(self, Nin, Nout):
        assert isinstance(Nin, int)
        assert isinstance(Nout, int)
        #Glorot uniform
        bound = np.sqrt(6./(Nin+Nout))
        self.W = ss.truncnorm.rvs(
            -bound, bound, size=Nin*Nout).reshape(Nin, Nout)
        self.shape = (Nin, Nout)

    def forward(self, X):
        z = np.dot(X, self.W)
        self.A = _sigmoid(z)
        self.dAdz = _sigmoid_deriv(z)
        return self.A

    def backward(self, X, NextLayer):
        print(NextLayer.delta.shape, NextLayer.W.shape, self.dAdz.shape)

        temp = np.dot(NextLayer.delta, NextLayer.W)
        print(temp.shape)
        self.delta = temp * self.dAdz.T[:]
        return self.delta

    def update(self, lA, learning_rate):
        res = np.dot(lA, self.delta)
        print(res.shape)
        #self.W -= learning_rate * res

class SoftmaxLayer(object):
    def __init__(self, N):
        assert isinstance(N, int)
        self.N = N
        self.W = np.ones(N) #no weights

    def forward(self, X):
        self.p = _softmax(X)
        return self.p
        
    def backward(self, X, y):
        #Derivative of cross entropy loss
        #Assume y is a one-hot encoding

        m = y.shape[0]
        self.loss = _softmax(X)
        grad = self.loss
        grad[range(m), y] -= y
        grad /= m
        self.delta = grad
        return grad

    def update(self, lA, learning_rate):
        pass
        
class myNN(object):
    def __init__(self, input_shape, Nlayers, nodes,
                 learning_rate = 1e-4, classifier = False):
        assert isinstance(input_shape, int)
        assert isinstance(Nlayers, int)
        assert isinstance(learning_rate, float)
        if not isinstance(nodes, (list, tuple)):
            nodes = (nodes,) * Nlayers
        assert Nlayers == len(nodes)
        self.input_shape = input_shape
        self.Nlayers = Nlayers
        self.nodes = nodes
        self.classifier = classifier
        self.learning_rate = learning_rate

        layers = []
        for i in range(self.Nlayers):
            if i == 0:
                #print(f"Dense at layer {i} with {nodes[i]} nodes")
                layers.append(DenseLayer(input_shape+1, nodes[i]))
            else:
                #print(f"Dense at layer {i} with {nodes[i]} nodes")
                layers.append(DenseLayer(nodes[i-1], nodes[i]))
        if self.classifier:
            #print(f"SM at layer {self.Nlayers} with {nodes[i]} nodes")
            layers.append(SoftmaxLayer(nodes[-1]))
        self.layers = layers

    def loss(self, X, y):
        #Cross entropy loss
        y = np.atleast_2d(y)
        m = y.shape[0]
        self.layers[-1].forward(X)
        p = self.layers[-1].p
        log_likelihood = -np.log(p[range(m), y])
        return np.sum(log_likelihood) / m

    def predict(self, X):
        X = np.atleast_2d(X)
        ones = np.atleast_2d(np.ones(X.shape[0]))
        assert (X.shape[-1] == self.input_shape)
        X = np.concatenate((ones.T, X), axis = 1) #the bias
        
        y = self.layers[0].forward(X)
        for l in self.layers[1:]:
            y = l.forward(y)
        return y

    def train(self, X, y, epochs=1):
        X = np.atleast_2d(X)
        ones = np.atleast_2d(np.ones(X.shape[0]))
        assert (X.shape[-1] == self.input_shape)
        X = np.concatenate((ones.T, X), axis = 1) #the bias

        y = np.asarray(y, dtype=int)
        y = y.reshape(len(y), 1)

        for k in range(epochs):
            a = X
            for l in self.layers:
                a = l.forward(a)

            delta = self.layers[-1].backward(a, y)
            print(len(self.layers))
            for l in range(self.Nlayers-1, -1, -1):
                print("on layer ", l, type(self.layers[l]))
                delta = self.layers[l].backward(delta, self.layers[l+1])

            a = X
            for l in self.layers[:-1]:
                l.update(self.learning_rate, a)
                a = layer.A

if __name__ == "__main__":
    NN = myNN(784, 3, [100, 50, 10], classifier=True)

    k = 100
    x = np.random.rand(784*k).reshape(k, 784)#X_train[0]
    y = np.random.randint(0, 10, k)
    y_est = NN.predict(x)
    print(y_est.shape, type(y))
    NN.train(x, y)
