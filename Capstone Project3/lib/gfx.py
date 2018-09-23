import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='ticks')

def plot_actual_vs_predicted(y, y_test, y_pred):
    """
    Displays two scatter plots of the actual visitation data to compare against the predicted data. 
    The right plot zooms in the data.
    """
    plt.figure(figsize=(17,6))

    plt.subplot(1, 2, 1)
    plt.scatter(y_test, y_pred, s=15, alpha=0.3, color='blue') 
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r-', lw=1)
    plt.title('Actual Fare data vs Predicted Fare')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')

    plt.subplot(1, 2, 2)
    plt.scatter(y_test, y_pred, s=10, alpha=0.3, color='blue') 
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r-', lw=1)
    plt.title('Actual Fare data vs Predicted Fare (zoom)')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.xlim(xmin=0, xmax=120)
    plt.ylim(ymin=0, ymax=120)

    plt.show()


import matplotlib.patches as mpatches
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import f_regression
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFECV
from itertools import compress

def get_feature_association_list(df, feature_names):
    """
    Returns a list with the F-Score of every feature to show the level of association with its target.
    """
    X = df[feature_names]
    y = df.visitors

    selector_f = SelectPercentile(f_regression, percentile=25)
    selector_f.fit(X,y)

    zipped_list = zip(feature_names, selector_f.scores_)
    zipped_list = sorted(zipped_list, key=lambda x: x[1])
    return reversed(zipped_list) # most important features are at the beginning of the list        
        

def get_feature_contribution_list(df, feature_names):
    """
    Returns a list with the names of the optimal features.
    This function helps choose features based on their effective contribution. It automatically reduces 
    the number of features involved in a learning model on the basis of their effective contribution to 
    the performance measured by the error measure.
    """
    X = df[feature_names]
    y = df.visitors
    
    reg = LinearRegression(normalize=True) 
    selector = RFECV(estimator=reg, cv=5, scoring='neg_mean_squared_error')
    selector.fit(X, y)
    return  list(compress(feature_names, selector.support_)) # size =  selector.n_features_


def plot_feature_importance(df, feature_names, side_by_side):
    feature_contrib_list = get_feature_contribution_list(df, feature_names)
#     print('feature_contrib_list=', feature_contrib_list)
    
    # convert a list of tuples (name, fscore) into a DataFrame
    d = dict(get_feature_association_list(df, feature_names))
#     print('dict=', d.items(), '\nvalues=', list(d.values()), '\ncolumn names=', list(d.keys()))

    fscore_df = pd.DataFrame(list(d.items()), columns=['features', 'f-score'])    
    
    # 'optimal' stores the results from get_feature_contribution_list() as True (yes) or False (no), 
    # indicating that the feature should be kept as part of the Optimal Features List and thus used for regression.
#     feature_contrib_list = feature_contrib_list[:-1] # DEBUG
    keep_list = []
    for feature, fscore in d.items():
        if feature in feature_contrib_list:
            keep_list.append('yes')
        else:
            keep_list.append('no')
    
    fscore_df['optimal'] = keep_list
#     display(fscore_df)
        
    if (not side_by_side):
        plt.figure(figsize=(13, 9)) 
    else:
        plt.subplot(1, 2, 2)
    
    colors = {'yes':'blue', 'no':'red'}
    ax = plt.scatter(fscore_df['f-score'], fscore_df['features'], c=fscore_df['optimal'].apply(lambda x: colors[x]), alpha=0.7)
    plt.title('Feature Contribution and Association (F-Score)')
#     plt.ylabel('Features')
    plt.xlabel('F-Score')

    # Create custom legend
    colors = ["blue", "red"]
    texts  = ["Optimal Feature", "Bad Feature"]
    patches = [ plt.plot([],[], marker="o", ms=7, ls="", mec=None, color=colors[i], alpha=0.7, label="{:s}".format(texts[i]) )[0]  for i in range(len(texts)) ]
    plt.legend(handles=patches, fontsize=11)
    
    plt.gca().yaxis.grid(True) # enable horizontal grid lines
    
    if (not side_by_side):
        plt.show()
