import pandas as pd
import numpy as np


#separating file by a delimiter (any # of continuous spaces) so it can be read by pandas
#resetting the index since i am grouping by the index (precautionary)
qassoc = pd.read_csv("filtered_out_MAF0.txt", sep=r"\s+", lineterminator='\n', engine='python').reset_index(drop=True)

#drop all columns I cant take an average for, inplace means i dont have to qassoc=qassoc.drop
qassoc.drop(labels=["NMISS","BETA","SE","R2","T"], axis = 1, inplace= True)
#take -log of p column 
qassoc.P = -(np.log10(qassoc.P))

qassoc.reset_index(drop=True, inplace= True)


#creating empty dataframe to append to
df = pd.DataFrame(columns = qassoc.columns)

#group by chr
#remove the tail end of each chr so you can group by 21

for chrNum in qassoc.CHR.unique():
    sub_qassoc=qassoc[qassoc.CHR==chrNum].reset_index(drop=True)
    
    #removing tail end to avoid windows having less than 21 snps  
    sub_qassoc_odd = sub_qassoc.drop(sub_qassoc.tail(sub_qassoc.CHR.count() % 21).index)
  
    #starting at 10th row to begin overlapping windows
    #removing tail end to avoid overlapping windows having less than 21 snps  
    sub_qassoc_even = sub_qassoc.iloc[10:].reset_index(drop=True)
    sub_qassoc_even = sub_qassoc_even.drop(sub_qassoc_even.tail(sub_qassoc_even.CHR.count() % 21).index)
    

    sub_qassoc_oddSNP = sub_qassoc_odd.groupby(sub_qassoc_odd.index//21).apply(lambda x: x.loc[np.ceil(np.median(x.index.tolist()))])
   
    #start_BP_odd = pd.DataFrame(sub_qassoc_odd.groupby(sub_qassoc_odd.index//21).first().BP, columns=['BP']).reset_index(drop=True)
    #end_BP_odd = pd.DataFrame(sub_qassoc_odd.groupby(sub_qassoc_odd.index//21).tail(1).BP, columns=['BP']).reset_index(drop=True)
   
    #taking middle SNP of each window
    sub_qassoc_evenSNP = sub_qassoc_even.groupby(sub_qassoc_even.index//21).apply(lambda x: x.loc[np.ceil(np.median(x.index.tolist()))])  

    #storing first 
    #start_BP_even = pd.DataFrame(sub_qassoc_even.groupby(sub_qassoc_even.index//21).first().BP, columns=['BP']).reset_index(drop=True)
    #end_BP_even = pd.DataFrame(sub_qassoc_even.groupby(sub_qassoc_even.index//21).tail(1).BP, columns=['BP']).reset_index(drop=True)
    
    sub_qassoc_odd = sub_qassoc_odd.drop("SNP", axis = 1)
    sub_qassoc_even = sub_qassoc_even.drop("SNP", axis = 1)

    # sub_qassoc_odd = sub_qassoc_odd.drop("BP", axis = 1)
    # sub_qassoc_even = sub_qassoc_even.drop("BP", axis = 1)

    #taking average of -log10(p) values
    sub_qassoc_odd =sub_qassoc_odd.groupby(sub_qassoc_odd.index//21).mean()
    sub_qassoc_even =sub_qassoc_even.groupby(sub_qassoc_even.index//21).mean()

    #putting SNPs back in the dataframes
    sub_qassoc_odd["SNP"] = sub_qassoc_oddSNP["SNP"]
    sub_qassoc_even["SNP"] = sub_qassoc_evenSNP["SNP"]


    #sub_qassoc_odd["Starting BP"] = start_BP_odd["BP"]
    #sub_qassoc_odd["Ending BP"] = end_BP_odd["BP"]
   
    #sub_qassoc_even["Starting BP"] = start_BP_even["BP"]
    #sub_qassoc_even["Ending BP"] = end_BP_even["BP"]
    

    temp= pd.concat([sub_qassoc_odd, sub_qassoc_even]).sort_index()
    df = pd.concat([df, temp])
    

  
#df.drop(labels=["index"], axis = 1, inplace= True)

sigSNPs = df[df.P > 2.03]
sigSNPs.to_csv("sigSNPs2.csv")
df.to_csv("windowedBP2.csv", index=False)