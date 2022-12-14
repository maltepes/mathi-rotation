import sys
import pandas as pd
import numpy as np

def updatingFAM(fam, meta):

    filename = "allbrit.fam"
    updatedFAM = pd.read_csv(fam)
    pheno = pd.read_csv(meta)
   
    pheno = pheno.set_index('IID')
    pheno = pheno.reindex(index=updatedFAM['IID'])
    pheno = pheno.reset_index()

    print(pheno.IID.equals(updatedFAM.IID))

    updatedFAM['PHENO'] = pheno['DateBP']
    updatedFAM['PHENO'] = updatedFAM['PHENO'].astype(int)
    updatedFAM.to_csv(filename, header=None,index=False, sep= ' ', lineterminator='\n')

    
if __name__ == '__main__':
    fam = sys.argv[1]
    meta = sys.argv[2]
    updatingFAM(fam, meta)