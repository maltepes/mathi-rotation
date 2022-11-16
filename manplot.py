import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def manplot(filename):

    df = pd.read_csv(filename)

    # if the pvalue column is not already in -log form
    #df['-logp'] = - np.log(df["P"])

    running_pos = 0

    cumulative_pos = []

    for chrom, group_df in df.groupby("CHR"):
        cumulative_pos.append(group_df["BP"] + running_pos)
        running_pos += group_df["BP"].max()

    df["cumulative_pos"] = pd.concat(cumulative_pos)

    df['SNP number'] = df.index

    sns.relplot(
        data=df.sample(100000),
        x='cumulative_pos',
        y='P',
        aspect=4,
        hue='CHR',
        palette='Set1'
    )

    # show the graph
    plt.show()


if __name__ == '__main__':
    filename = sys.argv[1]
    manplot(filename)
