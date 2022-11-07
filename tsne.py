from sklearn.datasets import fetch_openml
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt

colors = ["black", "lightgray", "red", "saddlebrown", "darkorange", "steelblue", "yellow", "green", "lime", "cyan",
          "blue", "purple", "deeppink", "crimson", "chartreuse", "maroon", "springgreen", "indigo", "lightcoral"]


def tsne(distMat, label, nIter) :

    X = distMat

    # Randomly select 1000 samples for performance reasons
    # np.random.seed(100)
    # subsample_idc = np.random.choice(X.shape[0], 1000, replace=False)
    # X = X[subsample_idc,:]
    # label = label[subsample_idc]

    # Generating unique Label list
    uniqueLabel = list(set(label))
    uniqueLabel.sort()

    tsne = TSNE(2, perplexity=20, metric="precomputed", n_iter=nIter) # TSNE settings have to be set here according to : https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html#examples-using-sklearn-manifold-tsne
    tsne_result = tsne.fit_transform(X) # Apply TSNE

    fig, ax = plt.subplots(1)

    label= np.array(label)
    i=0
    for g in uniqueLabel:
        ix = np.where(label == g)
        plt.scatter(tsne_result[ix,0], tsne_result[ix,1], s=5, c=colors[i], label=g)
        i+=1
    lim = (tsne_result.min()-5, tsne_result.max()+5)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_aspect('equal')
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.show()