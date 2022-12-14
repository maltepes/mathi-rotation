import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from qmplot import qqplot
from manplot import *
from sigSNPsTable import *

# averaging -logp values of 21 snps in each window (overlapping)


def overlapping(filename, OL_StartEndBP):

    # separating file by a delimiter (any # of continuous spaces) so it can be read by pandas
    # resetting the index since i am grouping by the index (precautionary)

    #qassoc = pd.read_csv("allbrit_imputed.txt", sep=r"\s+", lineterminator='\n', engine='python').reset_index(drop=True)

    #making it so the imputed data only has the SNPs that the psuedohaploid MAF > 10% has
    preQA = pd.read_csv("allbrit_imputedLINpreQA.txt", sep=r"\s+", lineterminator='\n', engine='python').reset_index(drop=True)
    SNPsToFilter = pd.read_csv("filtered_out_MAFboth10.txt", sep=r"\s+", lineterminator='\n', engine='python').reset_index(drop=True)
    
    preQA = preQA.dropna(subset=["P"])

    qassoc = pd.DataFrame(columns=preQA.columns)

    qassoc = preQA[(preQA.SNP.isin(SNPsToFilter.SNP))].reset_index(drop=True)

    qassoc.to_csv("LIN_reattemptedImputed_postQA.csv", index=False)
    

    # drop all columns I cant take an average for
    qassoc.drop(labels=["NMISS", "BETA", "SE", "R2", "T"],
                axis=1, inplace=True)

    # take -log of p column if need be
    qassoc.P = -(np.log10(qassoc.P))

    qassoc.reset_index(drop=True, inplace=True)

    # creating empty dataframe to append to
    df = pd.DataFrame(columns=qassoc.columns)

    # group by chr
    # remove the tail end of each chr so you can group by 21

    for chrNum in qassoc.CHR.unique():
        sub_qassoc = qassoc[qassoc.CHR == chrNum].reset_index(drop=True)

        # removing tail end to avoid windows having less than 21 snps
        sub_qassoc_odd = sub_qassoc.drop(
            sub_qassoc.tail(sub_qassoc.CHR.count() % 21).index)

        # starting at 10th row to begin overlapping windows
        # removing tail end to avoid overlapping windows having less than 21 snps
        sub_qassoc_even = sub_qassoc.iloc[10:].reset_index(drop=True)
        sub_qassoc_even = sub_qassoc_even.drop(
            sub_qassoc_even.tail(sub_qassoc_even.CHR.count() % 21).index)

        sub_qassoc_oddSNP = sub_qassoc_odd.groupby(
            sub_qassoc_odd.index//21).apply(lambda x: x.loc[np.ceil(np.median(x.index.tolist()))])

        if OL_StartEndBP:
            start_BP_odd = pd.DataFrame(sub_qassoc_odd.groupby(
                sub_qassoc_odd.index//21).first().BP, columns=['BP']).reset_index(drop=True)
            end_BP_odd = pd.DataFrame(sub_qassoc_odd.groupby(
                sub_qassoc_odd.index//21).tail(1).BP, columns=['BP']).reset_index(drop=True)

        # taking middle SNP of each window
        sub_qassoc_evenSNP = sub_qassoc_even.groupby(
            sub_qassoc_even.index//21).apply(lambda x: x.loc[np.ceil(np.median(x.index.tolist()))])

        if OL_StartEndBP:
            start_BP_even = pd.DataFrame(sub_qassoc_even.groupby(
                sub_qassoc_even.index//21).first().BP, columns=['BP']).reset_index(drop=True)
            end_BP_even = pd.DataFrame(sub_qassoc_even.groupby(
                sub_qassoc_even.index//21).tail(1).BP, columns=['BP']).reset_index(drop=True)

        sub_qassoc_odd = sub_qassoc_odd.drop("SNP", axis=1)
        sub_qassoc_even = sub_qassoc_even.drop("SNP", axis=1)

        if OL_StartEndBP:
            sub_qassoc_odd = sub_qassoc_odd.drop("BP", axis=1)
            sub_qassoc_even = sub_qassoc_even.drop("BP", axis=1)

        # taking mean of 21 snps in each window
        sub_qassoc_odd = sub_qassoc_odd.groupby(
            sub_qassoc_odd.index//21).mean()
        sub_qassoc_even = sub_qassoc_even.groupby(
            sub_qassoc_even.index//21).mean()

        # putting SNPs back in the dataframes
        sub_qassoc_odd["SNP"] = sub_qassoc_oddSNP["SNP"]
        sub_qassoc_even["SNP"] = sub_qassoc_evenSNP["SNP"]

        if OL_StartEndBP:
            sub_qassoc_odd["Starting BP"] = start_BP_odd["BP"]
            sub_qassoc_odd["Ending BP"] = end_BP_odd["BP"]

            sub_qassoc_even["Starting BP"] = start_BP_even["BP"]
            sub_qassoc_even["Ending BP"] = end_BP_even["BP"]

        temp = pd.concat([sub_qassoc_odd, sub_qassoc_even]).sort_index()
        df = pd.concat([df, temp])

    #df.drop(labels=["index"], axis = 1, inplace= True)

    # needed to create sig SNP tables
    sigSNPs = df[df.P > 3.0]
    sigSNPs.to_csv("sigSNPs_" + filename)

    df.to_csv(filename, index=False)

    if not OL_StartEndBP:
        # remember to change if the p value column is already -log
        #ax = qqplot(data=df["P"])
        ax = qqplot(data=10**-(df["P"]))
        plt.savefig("QQ" + filename + ".png")
        # manplot(filename)

    else:
        sigSNPsTable("sigSNPs_" + filename)


if __name__ == '__main__':
    filename = sys.argv[1]
    OL_StartEndBP = sys.argv[2].upper() == "True".upper()
    overlapping(filename, OL_StartEndBP)
