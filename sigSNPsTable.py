import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def sigSNPsTable(filename):

    df = pd.read_csv(filename)
    
    table = pd.DataFrame(columns=["CHR", "Starting BP", "Ending BP", "Target SNP", "P"])
    
    for chrNum in df.CHR.unique():
        count = 1
        # staying within same chromosome
        sub_df = df[df.CHR == chrNum].reset_index(drop=True)
        
        sub_df["difference"] = sub_df["Starting BP"] - sub_df["Ending BP"].shift(1)

        sub_df["group"] = 0
        sub_df.difference = sub_df.difference.fillna(0)
        idx_df = sub_df[sub_df.difference > 1000000]
        for idx in idx_df.index.values:
            sub_df.loc[idx:,"group"] = count
            count+=1

        groupedDF = sub_df.groupby("group").agg({"Starting BP":"first", "Ending BP": "last", "P": "max", "CHR": "first"})

        for groupNum in sub_df.group.unique():
            sub_sub_df = sub_df[sub_df.group == groupNum]
            groupedDF.loc[groupNum,"Target SNP"] = sub_sub_df.loc[sub_sub_df.P.idxmax()].SNP
            
        
        table = pd.concat([table, groupedDF])
        
    table.to_csv("output.csv", index=False)


if __name__ == '__main__':
    filename = sys.argv[1]
    sigSNPsTable(filename)
