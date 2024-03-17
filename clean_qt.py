"""Load and clean the Quizzes Tests dataframe"""

import argparse
import pandas as pd
import numpy as np

def qt_load_clean(path_qt):

    """Add the following features to the df:
        - weighted_score.
        - percentage of tp submitted.
        - percentage of tp submitted on time"""

    qt= pd.read_csv(f'{path_qt}')

    qt_1= qt[qt["due_date"] <= 60]

    qt_1["weighted_score"]= qt_1["weight"] * qt_1["score"] / 100

    qt_2= qt_1[["id_student", "weighted_score"]]

    grouped= qt_2["weighted_score"].groupby(qt_2["id_student"])

    qt_4= grouped.mean()

    qt_4= qt_4.reset_index()

    #Submitted all quizzes and tests

    qt_5= qt_1[["id_student", "assignment_name", "date_submitted"]]

    qt_5["sum_submitted"]= np.where(qt_5["date_submitted"].isnull(), 0, 1)

    grouped= qt_5["sum_submitted"].groupby(qt_5["id_student"])

    qt_7= grouped.sum()

    qt_7= qt_7.reset_index()

    qt_7["submitted"]= qt_7["sum_submitted"] / 4

    qt_8= qt_7.drop(['sum_submitted'], axis=1)

    #Submission on time

    qt_9= qt_1.copy()

    qt_9["date_submitted"]= qt_9["date_submitted"].fillna(99)

    qt_9["submission_ondate_sum"]= np.where(qt_9["date_submitted"] > qt_9["due_date"], 0, 1)

    qt_10= qt_9[["id_student","assignment_name", "submission_ondate_sum"]]

    grouped= qt_10["submission_ondate_sum"].groupby(qt_10["id_student"])

    qt_12= grouped.sum()

    qt_12= qt_12.reset_index()

    qt_12["submission_ondate"]= qt_12["submission_ondate_sum"] / 4

    qt_13= qt_12.drop(['submission_ondate_sum'], axis=1)

    #Join everything

    qt_coded_1= pd.merge(qt_4, qt_8, on= "id_student", how= "left")

    qt_coded= pd.merge(qt_coded_1, qt_13, on= "id_student", how= "left")

    return qt_coded

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('input_QT', type=str, help='Path to the QT file')

    args = parser.parse_args()

    input_data= args.input_QT

    QT_coded= qt_load_clean(input_data)
