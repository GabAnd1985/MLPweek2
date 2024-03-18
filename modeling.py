"""Generate two different models and graph the prediction probabilites of the two of them"""

import argparse
import warnings
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from clean_si import si_load_clean
from clean_qt import qt_load_clean
from clean_lr import lr_load_clean
warnings.filterwarnings("ignore")

def train_test_set_func():

    """Generate the train and test dataframes"""

    df_original_1= pd.merge(final_result, qt_coded, on= "id_student", how= "left")

    df_original_2= pd.merge(df_original_1, lr_coded, on= "id_student", how= "left")

    df_original= df_original_2.fillna(0)

    x = df_original.drop(['id_student', 'final_result'], axis=1)

    y = df_original['final_result']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    return x_train, x_test, y_train, y_test

def generate_pipe():

    """Generate the pipelines for the two models:
        - logistic regression.
        - Random forest."""

    continuous_features= ['submitted', 'submission_ondate',
                          'weighted_score', 'mean_clicks',
                          'course_homepage_totalclicks', 
                          'course_page_totalclicks', 'forum_totalclicks',
                          'resource_totalclicks', 'wiki_totalclicks']

    pipe= Pipeline([('scaler', StandardScaler())])

    logistic_regression = Pipeline(steps=[
        ('preprocessor', pipe),
        ('classifier', LogisticRegression(random_state=42))
    ])

    random_forest = Pipeline(steps=[
        ('preprocessor', pipe),
        ('classifier', RandomForestClassifier(random_state=42))
    ])

    return continuous_features, logistic_regression, random_forest

def graph_prediction_distribution(path_output):

    """fot models and graph the prediction
    probabilities using box plot"""

    logistic_regression_final.fit(x_train_final[continuous_features_final], y_train_final)

    random_forest_final.fit(x_train_final[continuous_features_final], y_train_final)

    y_proba_lr= logistic_regression_final.predict_proba(
        x_test_final[continuous_features_final])[:, 1]

    y_proba_rf= random_forest_final.predict_proba(x_test_final[continuous_features_final])[:, 1]

    data = [y_proba_lr, y_proba_rf]

    colors = ['blue', 'orange']

    # Create a boxplot
    plt.figure(figsize=(10, 6))
    bp = plt.boxplot(data, patch_artist=True, widths=0.5)

    # Set colors for each box
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    plt.xlabel('Model')
    plt.ylabel('Predicted Probability')
    plt.title('Distribution of Predicted Probabilities',
              fontsize=16, color='black', fontweight='bold')
    plt.xticks([1, 2], ['Logistic Regression', 'Random Forest'])
    plt.grid(True)
    plt.savefig(f'{path_output}')
    plt.show()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('input_SI', type=str, help='Path to the SI file')
    parser.add_argument('input_QT', type=str, help='Path to the QT file')
    parser.add_argument('input_LR', type=str, help='Path to the LR file')
    parser.add_argument('output', type=str, help='Path to the output file')

    args = parser.parse_args()

    final_result= si_load_clean(args.input_SI)

    qt_coded= qt_load_clean(args.input_QT)

    lr_coded= lr_load_clean(args.input_LR)

    x_train_final, x_test_final, y_train_final, y_test_final= train_test_set_func()

    continuous_features_final, logistic_regression_final, random_forest_final= generate_pipe()

    graph_prediction_distribution(args.output)
