import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

imputed = pd.read_csv("qassoc_imputed_postQA.txt", sep=r"\s+", lineterminator='\n', engine='python').reset_index(drop=True)
psuedohaploid = pd.read_csv("psuedohaploid.txt", sep=r"\s+", lineterminator='\n', engine='python').reset_index(drop=True)

pVal = pd.DataFrame(columns= ["imputedP", "psuedoP"])
pVal["imputedP"] = -(np.log10(imputed["P"]))
pVal["psuedoP"] = -(np.log10(psuedohaploid["P"]))

pVal.plot.scatter(x="psuedoP", y="imputedP", alpha=0.5)

plt.show()

tStat = pd.DataFrame(columns= ["imputedT", "psuedoT"])
tStat["imputedT"] = imputed["T"]
tStat["psuedoT"] = psuedohaploid["T"]

tStat.plot.scatter(x="psuedoT", y="imputedT", alpha=0.5)

plt.show()