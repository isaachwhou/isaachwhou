import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import f1_score, mean_squared_error, accuracy_score, average_precision_score, recall_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder

application_train = pd.read_csv("application_train.csv")

# Phone score
mobile_variable = ["FLAG_MOBIL", "FLAG_EMP_PHONE", "FLAG_WORK_PHONE", "FLAG_CONT_MOBILE", "FLAG_PHONE", "FLAG_EMAIL"]
mobile_data = application_train.loc[:,mobile_variable]
application_train["Mobile_score"] = mobile_data.sum(axis=1)
application_train = application_train.drop(mobile_variable, axis=1)

# Address score
address_variable = ["REG_REGION_NOT_LIVE_REGION", "REG_REGION_NOT_WORK_REGION", "LIVE_REGION_NOT_WORK_REGION", "REG_CITY_NOT_LIVE_CITY", "REG_CITY_NOT_WORK_CITY", "LIVE_CITY_NOT_WORK_CITY"]
address_data = application_train.loc[:,address_variable]
application_train["Address_score"] = address_data.sum(axis=1)
application_train = application_train.drop(address_variable, axis=1)

# REGION_RATING average
region_rating = application_train.loc[:,["REGION_RATING_CLIENT", "REGION_RATING_CLIENT_W_CITY"]]
application_train["Region_rating_avg"] = region_rating.mean(axis=1)
application_train = application_train.drop(region_rating, axis=1)

# Documentation score
documents_variable = [
    "FLAG_DOCUMENT_2",
    "FLAG_DOCUMENT_3",
    "FLAG_DOCUMENT_4",
    "FLAG_DOCUMENT_5",
    "FLAG_DOCUMENT_6",
    "FLAG_DOCUMENT_7",
    "FLAG_DOCUMENT_8",
    "FLAG_DOCUMENT_9",
    "FLAG_DOCUMENT_10",
    "FLAG_DOCUMENT_11",
    "FLAG_DOCUMENT_12",
    "FLAG_DOCUMENT_13",
    "FLAG_DOCUMENT_14",
    "FLAG_DOCUMENT_15",
    "FLAG_DOCUMENT_16",
    "FLAG_DOCUMENT_17",
    "FLAG_DOCUMENT_18",
    "FLAG_DOCUMENT_19",
    "FLAG_DOCUMENT_20",
    "FLAG_DOCUMENT_21",
]
documents_data = application_train.loc[:,documents_variable]
application_train["Documentation_score"] = documents_data.sum(axis=1)
application_train = application_train.drop(documents_variable, axis=1)

# Number of enquiries to Credit Bureau (one year)
cb_enquireies = [
    "AMT_REQ_CREDIT_BUREAU_HOUR", 
    "AMT_REQ_CREDIT_BUREAU_DAY", 
    "AMT_REQ_CREDIT_BUREAU_WEEK",
    "AMT_REQ_CREDIT_BUREAU_MON",
    "AMT_REQ_CREDIT_BUREAU_QRT",
    "AMT_REQ_CREDIT_BUREAU_YEAR",
]
cb_enquireies_data = application_train.loc[:,cb_enquireies]
application_train["AMT_REQ_CREDIT_BUREAU"] = cb_enquireies_data.sum(axis=1)
application_train = application_train.drop(cb_enquireies, axis=1)

# drop building normalized information
index_start = application_train.columns.get_loc('APARTMENTS_AVG')
index_end = application_train.columns.get_loc('NONLIVINGAREA_MEDI')
building_normalized_info = application_train.iloc[:,index_start:index_end+1]
building_col_list = building_normalized_info.columns
application_train = application_train.drop(building_col_list, axis=1)

# calculate credit income percentage
application_train['CREDIT_INCOME_PER'] = application_train['AMT_CREDIT'] / application_train['AMT_INCOME_TOTAL']

# categorical data
obj_df = application_train.select_dtypes(include=['object']).copy()
obj_col = obj_df.columns
'''
['NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY',
       'NAME_TYPE_SUITE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE',
       'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'OCCUPATION_TYPE',
       'WEEKDAY_APPR_PROCESS_START', 'ORGANIZATION_TYPE', 'FONDKAPREMONT_MODE',
       'HOUSETYPE_MODE', 'WALLSMATERIAL_MODE', 'EMERGENCYSTATE_MODE']
'''
# for binary categorical data, we use label encoding.
encoder = LabelEncoder() 
for col in obj_col:
    if len(list(application_train[col].unique())) <= 2:
        encoder.fit(application_train[col])
        application_train[col] = encoder.transform(application_train[col])

# for others, use one-hot encoding.
application_train = pd.get_dummies(application_train, drop_first=True)

# find spearman pho
application_train = application_train.fillna(0)
corr = application_train.corr(method = 'spearman')
corr_target = abs(corr['TARGET'])
relevant_features = corr_target[corr_target>0.04]
relevant_features_list = list(relevant_features.index.values)
relevant_features_list.remove('TARGET')


'''
print(relevant_features_list)
['DAYS_BIRTH', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'TOTALAREA_MODE', 'DAYS_LAST_PHONE_CHANGE', 'Address_score', 'Region_rating_avg', 'CODE_GENDER_M', 'NAME_INCOME_TYPE_Pensioner', 'NAME_INCOME_TYPE_Working', 'NAME_EDUCATION_TYPE_Higher education', 'NAME_EDUCATION_TYPE_Secondary / secondary special', 'OCCUPATION_TYPE_Laborers', 'ORGANIZATION_TYPE_XNA']

DAYS_BIRTH                                           0.078328
DAYS_REGISTRATION                                    0.040171 
DAYS_ID_PUBLISH                                      0.052535 
EXT_SOURCE_1                                         0.048352
EXT_SOURCE_2                                         0.146677
EXT_SOURCE_3                                         0.121134
TOTALAREA_MODE                                       0.048451
DAYS_LAST_PHONE_CHANGE                               0.053709 
Address_score                                        0.047875
Region_rating_avg                                    0.060338
CODE_GENDER_M                                        0.054713
NAME_INCOME_TYPE_Pensioner                           0.046209
NAME_INCOME_TYPE_Working                             0.057481
NAME_EDUCATION_TYPE_Higher education                 0.056593
NAME_EDUCATION_TYPE_Secondary / secondary special    0.049824
OCCUPATION_TYPE_Laborers                             0.043019
ORGANIZATION_TYPE_XNA                                0.045987
'''




# TESTING

#corr.to_excel(r'C:\Users\Isaac\OneDrive\Documents\UNSW\COMP9417\Project\home-credit-default-risk\spearman.xlsx', index = True, header=True)

#f, ax = plt.subplots(figsize=(20, 18))
#mask = np.triu(np.ones_like(corr, dtype=bool))
#cmap = sns.diverging_palette(230, 20, as_cmap=True)
#sns.heatmap(corr, annot=True, mask = mask, cmap=cmap)
#plt.show()
#plt.savefig('1.png')


