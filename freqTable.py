import sys
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def freqTable(filename):

    freq = pd.read_csv(filename)
    freq.sort_values(by=["date"], ascending=False)
    freq["date"] = freq["date"].div(30).astype(int)
    freq["pseudo1"].replace("0", np.nan, inplace=True)
    freq["pseudo2"].replace("0", np.nan, inplace=True)
    
    fig = go.Figure()
    fig.update_xaxes(autorange = "reversed")
    fig.update_xaxes(range = [0,150])
    fig.update_yaxes(range = [0,1])



    bin_size = 50
    master = pd.DataFrame(columns=freq.columns)
    for time_bin in range(0, max(freq["date"]), bin_size):
        sub_df = freq[(freq["date"] >= time_bin) & (freq["date"] < time_bin + bin_size)]
        
        sub_df["grouped_date"] = sub_df["date"].mean()
        sub_df["imputed_freq"] = (sub_df[sub_df["imputed1"] == "A"].imputed1.count() + sub_df[sub_df["imputed2"] == "A"].imputed2.count()) / (sub_df["imputed1"].count() + sub_df["imputed2"].count())
        sub_df["pseudo_freq"] = (sub_df[sub_df["pseudo1"] == "A"].pseudo1.count() + sub_df[sub_df["pseudo2"] == "A"].pseudo2.count()) / (sub_df["pseudo1"].count() + sub_df["pseudo2"].count())
        
        master = pd.concat([master, sub_df])

    fig.add_trace(go.Scatter(
        x=master["grouped_date"],
        y=master["imputed_freq"],
        name="Imputed",
        mode="markers+lines",
        marker=dict(
            color="red",
            size=18
        ),
        line=dict(
            color="red"
        )
    ))

    fig.add_trace(go.Scatter(
        x=master["grouped_date"],
        y=master["pseudo_freq"],
        name="Pseudo",
        mode="markers+lines",
        marker=dict(
            color="blue",
            size=18
        ),
        line=dict(
            color="blue"
        )
    ))

    fig.write_html('freq.html', auto_open=True)


if __name__ == '__main__':
    filename = sys.argv[1]
    freqTable(filename)