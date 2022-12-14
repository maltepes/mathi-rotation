import pandas as pd

# separating all the files by a delimiter (any # of continuous spaces) so it can be read by pandas
modbrit = pd.read_csv("modbrit.txt", sep=r"\s+",
                      lineterminator='\n', engine='python')
ancbrit = pd.read_csv("ancbrit.txt", sep=r"\s+",
                      lineterminator='\n', engine='python')
qassoc = pd.read_csv("qassoc.txt", sep=r"\s+",
                     lineterminator='\n', engine='python')

modbrit = modbrit.dropna(subset=["MAF"])
print(modbrit.shape[0])

ancbrit = ancbrit.dropna(subset=["MAF"])
print(ancbrit.shape[0])

# MODBRIT
# removing the SNPs that have a <5% value for MAF, putting them into a new file just in case we want to see which ones

modbrit_5MAF = modbrit[(modbrit.MAF <= 0.05)].dropna(subset=["MAF"])
print(modbrit_5MAF.shape[0])

#filtered_mod = qassoc[(modbrit.SNP.isin(qassoc.SNP)) & ((modbrit.MAF != 0) & (modbrit.MAF != "NA"))].dropna(subset=["P"])

# Validation of filtering
# print(modbrit[(modbrit.MAF != 0) & (modbrit.MAF != "NA")].shape)
# print(filtered_mod.shape)

# Saving modbrit to csv
#filtered_mod.to_csv("filtered_mod.csv", index=False)

# ANCBRIT

# save snps with <5 MAF just in case
ancbrit_5MAF = ancbrit[(ancbrit.MAF <= 0.05)].dropna(subset=["MAF"])
print(ancbrit_5MAF.shape[0])


#filtered_anc = qassoc[(ancbrit.SNP.isin(qassoc.SNP)) & ((ancbrit.MAF != 0) & (ancbrit.MAF != "NA"))].dropna(subset=["P"])

# Validation of filtering
#print(ancbrit[(ancbrit.MAF != 0) & (ancbrit.MAF != "NA")].dropna().shape)
# print(filtered_anc.shape)

# Saving ancbrit to csv
#filtered_anc.to_csv("filtered_anc.csv", index=False)

# cross joining, saving them in separate files and also saving them together, would need to chunk them because it uses up a TiB of data
#mergedMod = pd.merge(modbrit, qassoc, how="cross")
#mergedAnc = pd.merge(ancbrit, qassoc, how="cross")

# filtering out both
filtered_out_MAF0 = qassoc[((ancbrit.SNP.isin(qassoc.SNP)) & ((ancbrit.MAF >= 0.1) & (ancbrit.MAF != "NA"))) & (
    (modbrit.SNP.isin(qassoc.SNP)) & ((modbrit.MAF >= 0.1) & (modbrit.MAF != "NA")))].dropna(subset=["P"])

# print(filtered_out_MAF0.shape[0])
#filtered_out_MAF0.to_csv("filtered_out_MAFboth10.csv", index=False)
