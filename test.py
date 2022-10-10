import pandas as pd
import os
import matplotlib.pyplot as plt

OutPath = r"D:\My Projects\UU\Remeshed"
remeshedDf = pd.read_csv(os.path.join(OutPath,"nVertices02.csv"))
df = pd.DataFrame(remeshedDf,columns=["index","class","fileName","beforeRemesh","afterRemesh"])
fig, axs = plt.subplots(1, 1,figsize=(10, 7),tight_layout=True)
plt.xlabel("nOfObjects")
plt.ylabel("nOfVerices")
plt.title('Numbers of verices after remeshing')
axs.hist(df["afterRemesh"], bins=10)
print(df["afterRemesh"].to_list())
plt.savefig(os.path.join(OutPath,"afterRemesh.png"))