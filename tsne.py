from sklearn.datasets import fetch_openml
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt

def tsne(distMat, label, nIter) :
    # Load the MNIST data
    # X, label = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False)

    X = distMat

    # Randomly select 1000 samples for performance reasons
    # np.random.seed(100)
    # subsample_idc = np.random.choice(X.shape[0], 1000, replace=False)
    # X = X[subsample_idc,:]
    # label = label[subsample_idc]

    # Generating unique Label list
    uniqueLabel = list(set(label))
    uniqueLabel.sort()
    # X row of Y features
    print(X.shape)
    # Label of each row of X
    print(len(label))
    # Label list
    print(uniqueLabel)

    tsne = TSNE(2, metric="precomputed", n_iter=nIter) # TSNE settings have to be set here according to : https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html#examples-using-sklearn-manifold-tsne
    tsne_result = tsne.fit_transform(X) # Apply TSNE

    fig, ax = plt.subplots(1)

    plt.scatter(tsne_result[:,0], tsne_result[:,1], s=5, c=[uniqueLabel.index(i) for i in label])
    lim = (tsne_result.min()-5, tsne_result.max()+5)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_aspect('equal')
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.show()