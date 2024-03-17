"""Load and clean the Learning Resources dataframe"""

import argparse
import pandas as pd

def lr_load_clean(path_lr):

    """Add the following features to the df:
        - mean clicks.
        - total clicks by resource."""

    lr= pd.read_csv(f'{path_lr}')

    lr_1= lr[lr["date"]<= 60]

    #--------------------------------------------------------------

    grouped= lr_1["sum_click"].groupby(lr_1["id_student"])

    lr_2= grouped.mean()

    lr_3= lr_2.reset_index()

    lr_4= lr_3.rename(columns= {"sum_click": "mean_clicks"})

    #--------------------------------------------------------------

    grouped= lr_1["sum_click"].groupby([lr_1["id_student"], lr_1["activity_type"]])

    lr_5= grouped.sum()

    lr_6= lr_5.reset_index()

    lr_6["activity_type_name"]= lr_6["activity_type"] + "_totalclicks"

    lr_7= lr_6.pivot(index='id_student', columns='activity_type_name', values='sum_click')

    lr_8= lr_7.reset_index()

    lr_9= lr_8.fillna(0)

    #--------------------------------------------------------------

    lr_coded= pd.merge(lr_4, lr_9, on= "id_student", how= "left")

    return lr_coded

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('input_LR', type=str, help='Path to the LR file')

    args = parser.parse_args()

    input_data= args.input_LR

    LR_coded= lr_load_clean(input_data)
