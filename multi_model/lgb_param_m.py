import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import ParameterGrid
import numpy as np
import matplotlib.pyplot as plt

train_feat=pd.read_csv('train_feat.csv')
train_label=train_feat['label'].values
train_feat.drop('label',inplace=True,axis=1)

validation_feat=pd.read_csv('validation_feat.csv')
validation_label=validation_feat['label'].values
validation_feat.drop('label',inplace=True,axis=1)
feat_names=list(train_feat.columns)

params = {
    'num_class':[max(train_label)+1],
    'objective': ['multiclass'],
    'learning_rate':[0.15],
    'feature_fraction': [0.8],
    'max_depth': [13],
    'num_leaves':[200],
    'bagging_fraction': [0.8],
    'bagging_freq':[5],
    'min_data_in_leaf':[15],
    'min_gain_to_split':[0],
    'num_iterations':[150],
    'lambda_l1':[0.01],
    'lambda_l2':[1],
    'verbose':[0],
    'is_unbalance':[True]
}
params=list(ParameterGrid(params))
lgbtrain=lgb.Dataset(train_feat,label=train_label,feature_name=feat_names)
lgbtest = validation_feat
for param in params:
    print(param)
    # model_cv=lgb.cv(param, lgbtrain, num_boost_round=param['num_iterations'], nfold=5, metrics='multi_error',verbose_eval=True)
    clf = lgb.train(param, lgbtrain, num_boost_round=param['num_iterations'])
    pred = clf.predict(lgbtest)
    predict_label=np.argmax(pred,axis=1)
    result=validation_label-predict_label
    print('acc:'+str(len(np.nonzero(result==0)[0])/result.shape[0]))
    # # feature importance
    # feature_importance=list(clf.feature_importance())
    # y_pos = np.arange(len(feat_names))
    # plt.barh(y_pos,feature_importance,align = 'center',alpha = 0.2,color='b')
    # plt.yticks(y_pos,feat_names)
    # plt.show()