"""Load and clean the Student Info dataframe"""

import argparse
import pandas as pd
import numpy as np

def si_load_clean(path_si):

    """We leave only the student ID and the final
       course outcome encoded as 1 (passed) or 0 (failed)"""

    si = pd.read_csv(f'{path_si}')

    final_result_1= si[["id_student", "final_result"]]

    final_result_2= final_result_1.drop_duplicates()

    final_result_2["final_result_1"]= np.where(final_result_2["final_result"]== "Fail", 0, 1)

    final_result_3= final_result_2.drop("final_result", axis= 1)

    final_result= final_result_3.rename(columns= {"final_result_1": "final_result"})

    return final_result

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('input_SI', type=str, help='Path to the SI file')

    args = parser.parse_args()

    input_data= args.input_SI

    SI_final_result= si_load_clean(input_data)
