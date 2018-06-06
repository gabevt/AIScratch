import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from mpl_toolkits.mplot3d import Axes3D
import tflearn

'''
iris = datasets.load_iris()
X = iris.data
y = iris.target

n_sample = len(X)
print("shape X: ", X.shape)
print("shape Y: ", y.shape)

input()


fig = plt.figure()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)


for name, label in [('Setosa', 0),
                    ('Versicolour', 1),
                    ('Virginica', 2)]:
    ax.text3D(X[y == label, 3].mean(),
              X[y == label, 0].mean(),
              X[y == label, 2].mean() + 2, name,
              horizontalalignment='center',
              bbox=dict(alpha=.2, edgecolor='w', facecolor='w'))
y = np.choose(y, [1, 2, 0]).astype(np.float)
ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y, edgecolor='k')
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
ax.set_title('Iris Dataset')
plt.show()
'''

def get_dataset(dataset_name):
    if dataset_name == "Boston":
        dset = datasets.load_boston()
        X = dset.data
        Y = dset.target
        return X,Y
    if dataset_name == "Iris":
        dset = datasets.load_iris()
        X = dset.data
        Y = dset.target
        return X,Y
    if dataset_name == "Diabetes":
        dset = datasets.load_diabetes()
        X = dset.data
        Y = dset.target
        return X,Y
    if dataset_name == "Digits":
        dset = datasets.load_digits()
        X = dset.data
        Y = dset.target
        return X,Y
    if dataset_name == "Wine":
        dset = datasets.load_wine()
        X = dset.data
        Y = dset.target
        return X,Y
    if dataset_name == "Breast_Cancer":
        dset = datasets.load_breast_cancer()
        X = dset.data
        Y = dset.target
        return X,Y
    if dataset_name == "Or":
        X = np.array([ [0,0], [1,0], [0,1], [1,1]])
        Y = np.array([[0], [1], [1], [1] ])
        return X,Y
    if dataset_name == "And":
        X = np.array([ [0,0], [1,0], [0,1], [1,1]])
        Y = np.array([[0], [0], [0], [1] ])
        return X,Y
    if dataset_name == "Xor":
        X = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
        Y = np.array([[0.], [1.], [1.], [0.]])
        return X,Y


#X,Y=get_dataset("Boston") #13 
#X,Y=get_dataset("Iris") # 4  
#X,Y=get_dataset("Diabetes") #10 
#X,Y=get_dataset("Digits") #64
#X,Y=get_dataset("Wine") #13   
X,Y=get_dataset("Breast_Cancer") # 30  
#X,Y=get_dataset("Or") #2 
#X,Y=get_dataset("And") #2   
#X,Y=get_dataset("Xor") #2         
print("shape X: ", X.shape)    
print("shape X: ", X.shape[-1])
print("shape Y: ", Y.shape)
Y=Y.reshape(len(Y),1)
print("shape Y: ", Y.shape)
input()
#Modelo
tnorm = tflearn.initializations.uniform(minval=-1., maxval=1.)
input_ = tflearn.input_data(shape=[None, X.shape[-1]])
hidden = tflearn.fully_connected(input_, n_units=110, activation='sigmoid', weights_init=tnorm)
hidden2 = tflearn.fully_connected(hidden, n_units=55, activation='sigmoid', weights_init=tnorm)
hidden3 = tflearn.fully_connected(hidden2, n_units=97, activation='sigmoid', weights_init=tnorm)
output = tflearn.fully_connected(hidden3, n_units=1, activation=None, name='output',  weights_init=tnorm)

regression = tflearn.regression(output, optimizer='sgd', loss='mean_square',
                                metric='accuracy', learning_rate=.5)

#Entrenamiento
m = tflearn.DNN(regression)
m.fit(X, Y.reshape(len(Y),1), n_epoch=50, show_metric=True, snapshot_epoch=False)





