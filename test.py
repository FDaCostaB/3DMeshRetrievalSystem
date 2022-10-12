import pandas as pd
import os
import matplotlib.pyplot as plt

labeledPath = r"D:\My Projects\UU\RemeshedPrinceton"
labeledPath = r"D:\My Projects\UU\RemeshedLabeledDB"
df = pd.read_csv(os.path.join(labeledPath,"nVertices.csv"))
afterRemesh = df["nOfVertices"]
fig, axs = plt.subplots(1, 1,figsize=(10, 7),tight_layout=True)
plt.xlabel("nOfVertices")
plt.ylabel("nOfObjects")
plt.title('Numbers of verices before remeshing')
axs.hist(afterRemesh, bins=20)
plt.savefig(os.path.join(labeledPath,"afterRemesh.png"))