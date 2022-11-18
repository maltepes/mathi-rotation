import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# adapted from
# https://github.com/mojones/video_notebooks/blob/master/Manhattan%20plots%20in%20Python.ipynb


def manplot(filename):

    df = pd.read_csv(filename)

    # if the pvalue column is not already in -log form
    df["-logP"] = -np.log(df["P"])

    #df["-logP"] = df["P"]

    running_BP = 0

    cumulative_BP = []

    for chrom, group_df in df.groupby("CHR"):
        cumulative_BP.append(group_df["BP"] + running_BP)
        running_BP += group_df["BP"].max()

    df["cumulative_BP"] = pd.concat(cumulative_BP)

    # df['SNP number'] = df.index

    df.CHR = df.CHR.astype(int)

    g = sns.relplot(
        #data=df.sample(100000, replace=True),
        data=df,
        x='cumulative_BP',
        y='-logP',
        aspect=3,
        hue='CHR',
        palette='Set1',
        linewidth=0,
        s=6,
        legend=None
    )

    g.ax.set_xlabel('Chromosome')
    g.ax.set_xticks(df.groupby('CHR')['cumulative_BP'].median())

    g.ax.set_xticklabels(df['CHR'].unique())
    #g.ax.axhline(5, linestyle='--', linewidth=1)

    g.fig.suptitle('Overlapping Windows')


# show the graph
    plt.ylim(0, 50)
    plt.savefig("manplot_" + filename + ".png")


if __name__ == '__main__':
    filename = sys.argv[1]
    manplot(filename)
