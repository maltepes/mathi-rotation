import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#checking difference between the two
imputed = pd.read_csv("qassoc_reattemptedImputed_postQA.txt", sep=r"\s+", lineterminator='\n', engine='python').reset_index(drop=True)
imputed2 = pd.read_csv("qassoc_imputed_postQA.txt", sep=r"\s+", lineterminator='\n', engine='python').reset_index(drop=True)
# diff = pd.concat([imputed1,imputed2]).drop_duplicates(keep=False)
#print(diff)


#imputed = pd.read_csv("qassoc_reattemptedImputed_postQA.txt", sep=r"\s+", lineterminator='\n', engine='python').reset_index(drop=True)
#psuedohaploid has the same SNPs as the imputed (original pseudohaploid qassoc file had more SNPs due to sex chromosomes and a larger bim file)
psuedohaploid = pd.read_csv("psuedohaploidSameSNPsAsImputed.txt", sep=r"\s+", lineterminator='\n', engine='python').reset_index(drop=True)

#checking if they both share the same SNPs 
print(imputed.SNP.equals(imputed2.SNP))
print(imputed.P.equals(imputed2.P))

print(imputed.SNP.equals(psuedohaploid.SNP))
print(imputed.P.equals(psuedohaploid.P))

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