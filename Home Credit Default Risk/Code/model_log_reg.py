'''
Feature selection / engineering on csv files
Prepare test file
Logistic Regression
5 fold cross validation used for fitting
Hyper-parameter Tuning
'''
import pandas as pd
import numpy as np
from sklearn import tree, preprocessing
import csv
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier
import time
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from statistics import mean

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score


if __name__ == '__main__':

    start = time.time()
    application_train = pd.read_csv('application_train.csv')

    # Feature selection / engineering on application_train.csv
    address_variable = ["REG_REGION_NOT_LIVE_REGION", "REG_REGION_NOT_WORK_REGION", "LIVE_REGION_NOT_WORK_REGION",
                        "REG_CITY_NOT_LIVE_CITY", "REG_CITY_NOT_WORK_CITY", "LIVE_CITY_NOT_WORK_CITY"]
    address_data = application_train.loc[:, address_variable]
    application_train["Address_score"] = address_data.sum(axis=1)
    application_train = application_train.drop(address_variable, axis=1)

    region_rating = application_train.loc[:, ["REGION_RATING_CLIENT", "REGION_RATING_CLIENT_W_CITY"]]
    application_train["Region_rating_avg"] = region_rating.mean(axis=1)
    application_train = application_train.drop(region_rating, axis=1)
    application_train['Region_rating_avg'] = region_rating.mean(axis=1)

    application_train['NAME_INCOME_TYPE_Working'] = application_train['NAME_INCOME_TYPE'].map(
        lambda x: 1 if x == 'Working' else 0)
    application_train['NAME_INCOME_TYPE_Pensioner'] = application_train['NAME_INCOME_TYPE'].map(
        lambda x: 1 if x == 'Pensioner' else 0)
    application_train['CODE_GENDER_M'] = application_train['CODE_GENDER'].map(lambda x: 1 if x == 'M' else 0)
    application_train['NAME_EDUCATION_TYPE_Secondary'] = application_train['NAME_EDUCATION_TYPE'].map(
        lambda x: 1 if x == 'Secondary / secondary special' else 0)
    application_train['NAME_EDUCATION_TYPE_Higher'] = application_train['NAME_EDUCATION_TYPE'].map(
        lambda x: 1 if x == 'Higher education' else 0)
    application_train['OCCUPATION_TYPE_Laborers'] = application_train['OCCUPATION_TYPE'].map(
        lambda x: 1 if x == 'Laborers' else 0)
    application_train['ORGANIZATION_TYPE_XNA'] = application_train['ORGANIZATION_TYPE'].map(
        lambda x: 1 if x == 'XNA' else 0)

    application_train = application_train[
        ['SK_ID_CURR', 'TARGET', 'DAYS_BIRTH', 'Region_rating_avg', 'NAME_INCOME_TYPE_Working', 'CODE_GENDER_M',
         'DAYS_LAST_PHONE_CHANGE', 'DAYS_ID_PUBLISH', 'NAME_EDUCATION_TYPE_Secondary',
         'Address_score', 'OCCUPATION_TYPE_Laborers', 'ORGANIZATION_TYPE_XNA', 'NAME_INCOME_TYPE_Pensioner',
         'EXT_SOURCE_1', 'TOTALAREA_MODE', 'NAME_EDUCATION_TYPE_Higher', 'EXT_SOURCE_3', 'EXT_SOURCE_2']]

    # Feature selection / engineering on bureau.csv
    bureau = pd.read_csv('bureau.csv')[['SK_ID_CURR','SK_ID_BUREAU','CREDIT_ACTIVE','DAYS_CREDIT','CREDIT_DAY_OVERDUE','DAYS_CREDIT_ENDDATE','AMT_CREDIT_MAX_OVERDUE','AMT_CREDIT_SUM','AMT_CREDIT_SUM_DEBT']]
    bureau_balance = pd.read_csv('bureau_balance.csv')
    bureau_balance_sorted = pd.DataFrame()
    bureau_balance_sorted['OCCURENCES']=bureau_balance.groupby('SK_ID_BUREAU').count()['MONTHS_BALANCE']
    bureau_balance_sorted['COUNT_1']=bureau_balance[bureau_balance['STATUS']=='1'].groupby('SK_ID_BUREAU')['STATUS'].count()
    bureau_balance_sorted['COUNT_2']=bureau_balance[bureau_balance['STATUS']=='2'].groupby('SK_ID_BUREAU')['STATUS'].count()
    bureau_balance_sorted['COUNT_3']=bureau_balance[bureau_balance['STATUS']=='3'].groupby('SK_ID_BUREAU')['STATUS'].count()
    bureau_balance_sorted['COUNT_4']=bureau_balance[bureau_balance['STATUS']=='4'].groupby('SK_ID_BUREAU')['STATUS'].count()
    bureau_balance_sorted['COUNT_5']=bureau_balance[bureau_balance['STATUS']=='5'].groupby('SK_ID_BUREAU')['STATUS'].count()
    bureau_balance_sorted=bureau_balance_sorted.fillna(0)
    bureau_balance_sorted['COUNT_ge1']=bureau_balance_sorted['COUNT_1']+bureau_balance_sorted['COUNT_2']+bureau_balance_sorted['COUNT_3']+bureau_balance_sorted['COUNT_4']+bureau_balance_sorted['COUNT_5']
    bureau_balance_sorted=bureau_balance_sorted.drop(['OCCURENCES','COUNT_1','COUNT_2','COUNT_3','COUNT_4','COUNT_5'], axis=1)

    bureau_merge = bureau.merge(bureau_balance_sorted, on='SK_ID_BUREAU', how='left')
    bureau_merge['COUNT_ge1'] = bureau_merge['COUNT_ge1'].fillna(0)
    bureau_sorted = pd.DataFrame()
    bureau_sorted['COUNT_ID'] = bureau_merge.groupby('SK_ID_CURR').count()['SK_ID_BUREAU']
    bureau_sorted['COUNT_ACTIVE'] = bureau_merge[bureau_merge['CREDIT_ACTIVE'] == 'Active'].groupby('SK_ID_CURR')[
        'CREDIT_ACTIVE'].count()
    bureau_sorted['COUNT_CLOSED'] = bureau_merge[bureau_merge['CREDIT_ACTIVE'] == 'Closed'].groupby('SK_ID_CURR')[
        'CREDIT_ACTIVE'].count()
    bureau_sorted['SUM_DAYS_CREDIT'] = bureau_merge.groupby('SK_ID_CURR')['DAYS_CREDIT'].sum()
    bureau_sorted['AVG_DAYS_CREDIT'] = bureau_sorted['SUM_DAYS_CREDIT'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_CREDIT_DAY_OVERDUE'] = bureau_merge.groupby('SK_ID_CURR')['CREDIT_DAY_OVERDUE'].sum()
    bureau_sorted['AVG_CREDIT_DAY_OVERDUE'] = bureau_sorted['SUM_CREDIT_DAY_OVERDUE'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_DAYS_CREDIT_ENDDATE'] = bureau_merge.groupby('SK_ID_CURR')['DAYS_CREDIT_ENDDATE'].sum()
    bureau_sorted['AVG_DAYS_CREDIT_ENDDATE'] = bureau_sorted['SUM_DAYS_CREDIT_ENDDATE'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_AMT_CREDIT_MAX_OVERDUE'] = bureau_merge.groupby('SK_ID_CURR')['AMT_CREDIT_MAX_OVERDUE'].sum()
    bureau_sorted['AVG_AMT_CREDIT_MAX_OVERDUE'] = bureau_sorted['SUM_AMT_CREDIT_MAX_OVERDUE'] / bureau_sorted[
        'COUNT_ID']
    bureau_sorted['SUM_AMT_CREDIT_SUM'] = bureau_merge.groupby('SK_ID_CURR')['AMT_CREDIT_SUM'].sum()
    bureau_sorted['AVG_AMT_CREDIT_SUM'] = bureau_sorted['SUM_AMT_CREDIT_SUM'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_AMT_CREDIT_SUM_DEBT'] = bureau_merge.groupby('SK_ID_CURR')['AMT_CREDIT_SUM_DEBT'].sum()
    bureau_sorted['AVG_AMT_CREDIT_SUM_DEBT'] = bureau_sorted['SUM_AMT_CREDIT_SUM_DEBT'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_AMT_CREDIT_SUM_REMAIN'] = bureau_sorted['SUM_AMT_CREDIT_SUM'] - bureau_sorted[
        'SUM_AMT_CREDIT_SUM_DEBT']
    bureau_sorted['AVG_AMT_CREDIT_SUM_REMAIN'] = bureau_sorted['SUM_AMT_CREDIT_SUM_REMAIN'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_COUNT_ge1'] = bureau_merge.groupby('SK_ID_CURR')['COUNT_ge1'].sum()
    bureau_sorted['AVG_COUNT_ge1'] = bureau_sorted['SUM_COUNT_ge1'] / bureau_sorted['COUNT_ID']
    bureau_sorted = bureau_sorted.drop(
        ['COUNT_ID', 'SUM_DAYS_CREDIT', 'SUM_CREDIT_DAY_OVERDUE', 'SUM_DAYS_CREDIT_ENDDATE',
         'SUM_AMT_CREDIT_MAX_OVERDUE', 'SUM_AMT_CREDIT_SUM', 'SUM_AMT_CREDIT_SUM_DEBT', 'SUM_AMT_CREDIT_SUM_REMAIN',
         'SUM_COUNT_ge1'], axis=1)
    master = application_train.merge(bureau_sorted, on='SK_ID_CURR', how='left')
    del (bureau)
    del (bureau_balance)
    del (bureau_sorted)

    # Feature selection / engineering on POS_CASH_balance.csv
    POS_CASH_balance = pd.read_csv('POS_CASH_balance.csv')[['SK_ID_PREV', 'SK_ID_CURR', 'MONTHS_BALANCE', 'SK_DPD_DEF']]
    POS_CASH_balance_sorted = pd.DataFrame()
    POS_CASH_balance_sorted = POS_CASH_balance.groupby('SK_ID_PREV').max('MONTHS_BALANCE')[
        ['SK_ID_CURR', 'MONTHS_BALANCE']]
    POS_CASH_balance_sorted['POS_CASH_OCCURENCES'] = POS_CASH_balance.groupby('SK_ID_PREV').count()['MONTHS_BALANCE']
    POS_CASH_balance_sorted['SUM_SK_DPD_DEF'] = POS_CASH_balance.groupby('SK_ID_PREV')['SK_DPD_DEF'].sum()
    POS_CASH_balance_sorted['AVG_SK_DPD_DEF'] = POS_CASH_balance_sorted['SUM_SK_DPD_DEF'] / POS_CASH_balance_sorted[
        'POS_CASH_OCCURENCES']
    POS_CASH_balance_sorted = POS_CASH_balance_sorted.drop(['MONTHS_BALANCE', 'SUM_SK_DPD_DEF'], axis=1)
    POS_CASH_balance_ID_CURR = POS_CASH_balance_sorted.groupby('SK_ID_CURR').sum()
    master = master.merge(POS_CASH_balance_ID_CURR, on='SK_ID_CURR', how='left')
    del (POS_CASH_balance)
    del (POS_CASH_balance_sorted)
    del (POS_CASH_balance_ID_CURR)

    # Feature selection / engineering on credit_card_balance.csv
    credit_card_balance = pd.read_csv('credit_card_balance.csv')
    credit_card_balance[['AMT_DRAWINGS_ATM_CURRENT', 'AMT_DRAWINGS_CURRENT', 'AMT_DRAWINGS_OTHER_CURRENT',
                         'AMT_DRAWINGS_POS_CURRENT']] = credit_card_balance[
        ['AMT_DRAWINGS_ATM_CURRENT', 'AMT_DRAWINGS_CURRENT', 'AMT_DRAWINGS_OTHER_CURRENT',
         'AMT_DRAWINGS_POS_CURRENT']].fillna(0)
    credit_card_balance[['CNT_DRAWINGS_ATM_CURRENT', 'CNT_DRAWINGS_CURRENT', 'CNT_DRAWINGS_OTHER_CURRENT',
                         'CNT_DRAWINGS_POS_CURRENT']] = credit_card_balance[
        ['CNT_DRAWINGS_ATM_CURRENT', 'CNT_DRAWINGS_CURRENT', 'CNT_DRAWINGS_OTHER_CURRENT',
         'CNT_DRAWINGS_POS_CURRENT']].fillna(0)
    credit_card_balance['AMT_DRAWINGS'] = credit_card_balance['AMT_DRAWINGS_ATM_CURRENT'] + credit_card_balance[
        'AMT_DRAWINGS_CURRENT'] + credit_card_balance['AMT_DRAWINGS_OTHER_CURRENT'] + credit_card_balance[
                                              'AMT_DRAWINGS_POS_CURRENT']
    credit_card_balance['CNT_DRAWINGS'] = credit_card_balance['CNT_DRAWINGS_ATM_CURRENT'] + credit_card_balance[
        'CNT_DRAWINGS_CURRENT'] + credit_card_balance['CNT_DRAWINGS_OTHER_CURRENT'] + credit_card_balance[
                                              'CNT_DRAWINGS_POS_CURRENT']
    credit_card_balance_sorted = pd.DataFrame()
    credit_card_balance_sorted = credit_card_balance.groupby('SK_ID_PREV').max('MONTHS_BALANCE')[['SK_ID_CURR']]
    credit_card_balance_sorted['AVG_AMT_BALANCE'] = credit_card_balance.groupby('SK_ID_PREV')['AMT_BALANCE'].sum() / \
                                                    credit_card_balance.groupby('SK_ID_PREV')['AMT_BALANCE'].count()
    credit_card_balance_sorted['CREDIT_COUNT_ACTIVE'] = \
    credit_card_balance[credit_card_balance['NAME_CONTRACT_STATUS'] == 'Active'].groupby('SK_ID_PREV')[
        'NAME_CONTRACT_STATUS'].count()
    credit_card_balance_ID_CURR = credit_card_balance_sorted.groupby('SK_ID_CURR').sum()
    master = master.merge(credit_card_balance_ID_CURR, on='SK_ID_CURR', how='left')
    del (credit_card_balance)
    del (credit_card_balance_sorted)
    del (credit_card_balance_ID_CURR)

    # Feature selection / engineering on installments_payments.csv
    installments_payments = pd.read_csv('installments_payments.csv')
    installments_payments['DIFF_DAY_PAYMENT'] = installments_payments['DAYS_ENTRY_PAYMENT'] - installments_payments[
        'DAYS_INSTALMENT']
    installments_payments['DIFF_AMT_PAYMENT'] = installments_payments['AMT_INSTALMENT'] - installments_payments[
        'AMT_PAYMENT']
    installments_payments_sorted = pd.DataFrame()
    installments_payments_sorted = installments_payments.groupby('SK_ID_PREV').max('MONTHS_BALANCE')[['SK_ID_CURR']]
    installments_payments_sorted['OCCURENCES'] = installments_payments.groupby('SK_ID_PREV').count()[
        'NUM_INSTALMENT_VERSION']
    installments_payments_sorted['SUM_DIFF_DAY_PAYMENT'] = installments_payments.groupby('SK_ID_PREV')[
        'DIFF_DAY_PAYMENT'].sum()
    installments_payments_sorted['AVG_DIFF_DAY_PAYMENT'] = installments_payments_sorted['SUM_DIFF_DAY_PAYMENT'] / \
                                                           installments_payments_sorted['OCCURENCES']
    installments_payments_sorted['SUM_DIFF_AMT_PAYMENT'] = installments_payments.groupby('SK_ID_PREV')[
        'DIFF_AMT_PAYMENT'].sum()
    installments_payments_sorted['AVG_DIFF_AMT_PAYMENT'] = installments_payments_sorted['SUM_DIFF_AMT_PAYMENT'] / \
                                                           installments_payments_sorted['OCCURENCES']
    installments_payments_sorted = installments_payments_sorted.drop(
        ['OCCURENCES', 'SUM_DIFF_DAY_PAYMENT', 'SUM_DIFF_AMT_PAYMENT'], axis=1)
    installments_payments_ID_CURR = installments_payments_sorted.groupby('SK_ID_CURR').sum()
    master = master.merge(installments_payments_ID_CURR, on='SK_ID_CURR', how='left')
    del (installments_payments)
    del (installments_payments_sorted)
    del (installments_payments_ID_CURR)

    # Feature selection / engineering on previous_application.csv
    previous_application = pd.read_csv('previous_application.csv')
    previous_application_sorted = pd.DataFrame()
    previous_application_sorted['COUNT_LOANS'] = previous_application.groupby('SK_ID_CURR')['SK_ID_PREV'].nunique()
    previous_application_sorted['COUNT_REVOLVING'] = \
    previous_application[previous_application['NAME_CONTRACT_TYPE'] == 'Revolving loans'].groupby('SK_ID_CURR')[
        'NAME_CONTRACT_TYPE'].count()
    previous_application_sorted['SUM_AMT_ANNUITY'] = previous_application.groupby('SK_ID_CURR')['AMT_ANNUITY'].sum()
    previous_application_sorted['AVG_AMT_ANNUITY'] = previous_application_sorted['SUM_AMT_ANNUITY'] / \
                                                     previous_application_sorted['COUNT_LOANS']
    previous_application_sorted['SUM_AMT_APPLICATION'] = previous_application.groupby('SK_ID_CURR')[
        'AMT_APPLICATION'].sum()
    previous_application_sorted['AVG_AMT_APPLICATION'] = previous_application_sorted['SUM_AMT_APPLICATION'] / \
                                                         previous_application_sorted['COUNT_LOANS']
    previous_application_sorted['AVG_DAYS_DECISION'] = previous_application.groupby('SK_ID_CURR')[
                                                           'DAYS_DECISION'].sum() / \
                                                       previous_application.groupby('SK_ID_CURR')[
                                                           'DAYS_DECISION'].count()
    previous_application_sorted['COUNT_REJECT'] = \
    previous_application[previous_application['CODE_REJECT_REASON'] != 'XAP'].groupby('SK_ID_CURR')[
        'CODE_REJECT_REASON'].count()
    previous_application_sorted[['COUNT_REVOLVING', 'COUNT_REJECT']] = previous_application_sorted[
        ['COUNT_REVOLVING', 'COUNT_REJECT']].fillna(0)
    master = master.merge(previous_application_sorted, on='SK_ID_CURR', how='left')
    del (previous_application)
    del (previous_application_sorted)
    master = master.drop(['SK_ID_CURR'], axis=1)

    # test data
    application_test = pd.read_csv('application_test.csv')

    address_variable = ["REG_REGION_NOT_LIVE_REGION", "REG_REGION_NOT_WORK_REGION", "LIVE_REGION_NOT_WORK_REGION",
                        "REG_CITY_NOT_LIVE_CITY", "REG_CITY_NOT_WORK_CITY", "LIVE_CITY_NOT_WORK_CITY"]
    address_data = application_test.loc[:, address_variable]
    application_test["Address_score"] = address_data.sum(axis=1)
    application_test = application_test.drop(address_variable, axis=1)

    region_rating = application_test.loc[:, ["REGION_RATING_CLIENT", "REGION_RATING_CLIENT_W_CITY"]]
    application_test["Region_rating_avg"] = region_rating.mean(axis=1)
    application_test = application_test.drop(region_rating, axis=1)
    application_test['Region_rating_avg'] = region_rating.mean(axis=1)

    application_test['NAME_INCOME_TYPE_Working'] = application_test['NAME_INCOME_TYPE'].map(
        lambda x: 1 if x == 'Working' else 0)
    application_test['NAME_INCOME_TYPE_Pensioner'] = application_test['NAME_INCOME_TYPE'].map(
        lambda x: 1 if x == 'Pensioner' else 0)
    application_test['CODE_GENDER_M'] = application_test['CODE_GENDER'].map(lambda x: 1 if x == 'M' else 0)
    application_test['NAME_EDUCATION_TYPE_Secondary'] = application_test['NAME_EDUCATION_TYPE'].map(
        lambda x: 1 if x == 'Secondary / secondary special' else 0)
    application_test['NAME_EDUCATION_TYPE_Higher'] = application_test['NAME_EDUCATION_TYPE'].map(
        lambda x: 1 if x == 'Higher education' else 0)
    application_test['OCCUPATION_TYPE_Laborers'] = application_test['OCCUPATION_TYPE'].map(
        lambda x: 1 if x == 'Laborers' else 0)
    application_test['ORGANIZATION_TYPE_XNA'] = application_test['ORGANIZATION_TYPE'].map(
        lambda x: 1 if x == 'XNA' else 0)

    application_test = application_test[
        ['SK_ID_CURR', 'DAYS_BIRTH', 'Region_rating_avg', 'NAME_INCOME_TYPE_Working', 'CODE_GENDER_M',
         'DAYS_LAST_PHONE_CHANGE', 'DAYS_ID_PUBLISH', 'NAME_EDUCATION_TYPE_Secondary',
         'Address_score', 'OCCUPATION_TYPE_Laborers', 'ORGANIZATION_TYPE_XNA', 'NAME_INCOME_TYPE_Pensioner',
         'EXT_SOURCE_1', 'TOTALAREA_MODE', 'NAME_EDUCATION_TYPE_Higher', 'EXT_SOURCE_3', 'EXT_SOURCE_2']]

    bureau = pd.read_csv('bureau.csv')[['SK_ID_CURR','SK_ID_BUREAU','CREDIT_ACTIVE','DAYS_CREDIT','CREDIT_DAY_OVERDUE','DAYS_CREDIT_ENDDATE','AMT_CREDIT_MAX_OVERDUE','AMT_CREDIT_SUM','AMT_CREDIT_SUM_DEBT']]
    bureau_balance = pd.read_csv('bureau_balance.csv')
    bureau_balance_sorted = pd.DataFrame()
    bureau_balance_sorted['OCCURENCES']=bureau_balance.groupby('SK_ID_BUREAU').count()['MONTHS_BALANCE']
    bureau_balance_sorted['COUNT_1']=bureau_balance[bureau_balance['STATUS']=='1'].groupby('SK_ID_BUREAU')['STATUS'].count()
    bureau_balance_sorted['COUNT_2']=bureau_balance[bureau_balance['STATUS']=='2'].groupby('SK_ID_BUREAU')['STATUS'].count()
    bureau_balance_sorted['COUNT_3']=bureau_balance[bureau_balance['STATUS']=='3'].groupby('SK_ID_BUREAU')['STATUS'].count()
    bureau_balance_sorted['COUNT_4']=bureau_balance[bureau_balance['STATUS']=='4'].groupby('SK_ID_BUREAU')['STATUS'].count()
    bureau_balance_sorted['COUNT_5']=bureau_balance[bureau_balance['STATUS']=='5'].groupby('SK_ID_BUREAU')['STATUS'].count()
    bureau_balance_sorted=bureau_balance_sorted.fillna(0)
    bureau_balance_sorted['COUNT_ge1']=bureau_balance_sorted['COUNT_1']+bureau_balance_sorted['COUNT_2']+bureau_balance_sorted['COUNT_3']+bureau_balance_sorted['COUNT_4']+bureau_balance_sorted['COUNT_5']
    bureau_balance_sorted=bureau_balance_sorted.drop(['OCCURENCES','COUNT_1','COUNT_2','COUNT_3','COUNT_4','COUNT_5'], axis=1)

    bureau_merge = bureau.merge(bureau_balance_sorted, on='SK_ID_BUREAU', how='left')
    bureau_merge['COUNT_ge1'] = bureau_merge['COUNT_ge1'].fillna(0)
    bureau_sorted = pd.DataFrame()
    bureau_sorted['COUNT_ID'] = bureau_merge.groupby('SK_ID_CURR').count()['SK_ID_BUREAU']
    bureau_sorted['COUNT_ACTIVE'] = bureau_merge[bureau_merge['CREDIT_ACTIVE'] == 'Active'].groupby('SK_ID_CURR')[
        'CREDIT_ACTIVE'].count()
    bureau_sorted['COUNT_CLOSED'] = bureau_merge[bureau_merge['CREDIT_ACTIVE'] == 'Closed'].groupby('SK_ID_CURR')[
        'CREDIT_ACTIVE'].count()
    bureau_sorted['SUM_DAYS_CREDIT'] = bureau_merge.groupby('SK_ID_CURR')['DAYS_CREDIT'].sum()
    bureau_sorted['AVG_DAYS_CREDIT'] = bureau_sorted['SUM_DAYS_CREDIT'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_CREDIT_DAY_OVERDUE'] = bureau_merge.groupby('SK_ID_CURR')['CREDIT_DAY_OVERDUE'].sum()
    bureau_sorted['AVG_CREDIT_DAY_OVERDUE'] = bureau_sorted['SUM_CREDIT_DAY_OVERDUE'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_DAYS_CREDIT_ENDDATE'] = bureau_merge.groupby('SK_ID_CURR')['DAYS_CREDIT_ENDDATE'].sum()
    bureau_sorted['AVG_DAYS_CREDIT_ENDDATE'] = bureau_sorted['SUM_DAYS_CREDIT_ENDDATE'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_AMT_CREDIT_MAX_OVERDUE'] = bureau_merge.groupby('SK_ID_CURR')['AMT_CREDIT_MAX_OVERDUE'].sum()
    bureau_sorted['AVG_AMT_CREDIT_MAX_OVERDUE'] = bureau_sorted['SUM_AMT_CREDIT_MAX_OVERDUE'] / bureau_sorted[
        'COUNT_ID']
    bureau_sorted['SUM_AMT_CREDIT_SUM'] = bureau_merge.groupby('SK_ID_CURR')['AMT_CREDIT_SUM'].sum()
    bureau_sorted['AVG_AMT_CREDIT_SUM'] = bureau_sorted['SUM_AMT_CREDIT_SUM'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_AMT_CREDIT_SUM_DEBT'] = bureau_merge.groupby('SK_ID_CURR')['AMT_CREDIT_SUM_DEBT'].sum()
    bureau_sorted['AVG_AMT_CREDIT_SUM_DEBT'] = bureau_sorted['SUM_AMT_CREDIT_SUM_DEBT'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_AMT_CREDIT_SUM_REMAIN'] = bureau_sorted['SUM_AMT_CREDIT_SUM'] - bureau_sorted[
        'SUM_AMT_CREDIT_SUM_DEBT']
    bureau_sorted['AVG_AMT_CREDIT_SUM_REMAIN'] = bureau_sorted['SUM_AMT_CREDIT_SUM_REMAIN'] / bureau_sorted['COUNT_ID']
    bureau_sorted['SUM_COUNT_ge1'] = bureau_merge.groupby('SK_ID_CURR')['COUNT_ge1'].sum()
    bureau_sorted['AVG_COUNT_ge1'] = bureau_sorted['SUM_COUNT_ge1'] / bureau_sorted['COUNT_ID']
    bureau_sorted = bureau_sorted.drop(
        ['COUNT_ID', 'SUM_DAYS_CREDIT', 'SUM_CREDIT_DAY_OVERDUE', 'SUM_DAYS_CREDIT_ENDDATE',
         'SUM_AMT_CREDIT_MAX_OVERDUE', 'SUM_AMT_CREDIT_SUM', 'SUM_AMT_CREDIT_SUM_DEBT', 'SUM_AMT_CREDIT_SUM_REMAIN',
         'SUM_COUNT_ge1'], axis=1)
    master_test = application_test.merge(bureau_sorted, on='SK_ID_CURR', how='left')
    del (bureau)
    del (bureau_balance)
    del (bureau_sorted)

    POS_CASH_balance = pd.read_csv('POS_CASH_balance.csv')[['SK_ID_PREV', 'SK_ID_CURR', 'MONTHS_BALANCE', 'SK_DPD_DEF']]
    POS_CASH_balance_sorted = pd.DataFrame()
    POS_CASH_balance_sorted = POS_CASH_balance.groupby('SK_ID_PREV').max('MONTHS_BALANCE')[
        ['SK_ID_CURR', 'MONTHS_BALANCE']]
    POS_CASH_balance_sorted['POS_CASH_OCCURENCES'] = POS_CASH_balance.groupby('SK_ID_PREV').count()['MONTHS_BALANCE']
    POS_CASH_balance_sorted['SUM_SK_DPD_DEF'] = POS_CASH_balance.groupby('SK_ID_PREV')['SK_DPD_DEF'].sum()
    POS_CASH_balance_sorted['AVG_SK_DPD_DEF'] = POS_CASH_balance_sorted['SUM_SK_DPD_DEF'] / POS_CASH_balance_sorted[
        'POS_CASH_OCCURENCES']
    POS_CASH_balance_sorted = POS_CASH_balance_sorted.drop(['MONTHS_BALANCE', 'SUM_SK_DPD_DEF'], axis=1)
    POS_CASH_balance_ID_CURR = POS_CASH_balance_sorted.groupby('SK_ID_CURR').sum()
    master_test = master_test.merge(POS_CASH_balance_ID_CURR, on='SK_ID_CURR', how='left')
    del (POS_CASH_balance)
    del (POS_CASH_balance_sorted)
    del (POS_CASH_balance_ID_CURR)

    credit_card_balance = pd.read_csv('credit_card_balance.csv')
    credit_card_balance[['AMT_DRAWINGS_ATM_CURRENT', 'AMT_DRAWINGS_CURRENT', 'AMT_DRAWINGS_OTHER_CURRENT',
                         'AMT_DRAWINGS_POS_CURRENT']] = credit_card_balance[
        ['AMT_DRAWINGS_ATM_CURRENT', 'AMT_DRAWINGS_CURRENT', 'AMT_DRAWINGS_OTHER_CURRENT',
         'AMT_DRAWINGS_POS_CURRENT']].fillna(0)
    credit_card_balance[['CNT_DRAWINGS_ATM_CURRENT', 'CNT_DRAWINGS_CURRENT', 'CNT_DRAWINGS_OTHER_CURRENT',
                         'CNT_DRAWINGS_POS_CURRENT']] = credit_card_balance[
        ['CNT_DRAWINGS_ATM_CURRENT', 'CNT_DRAWINGS_CURRENT', 'CNT_DRAWINGS_OTHER_CURRENT',
         'CNT_DRAWINGS_POS_CURRENT']].fillna(0)
    credit_card_balance['AMT_DRAWINGS'] = credit_card_balance['AMT_DRAWINGS_ATM_CURRENT'] + credit_card_balance[
        'AMT_DRAWINGS_CURRENT'] + credit_card_balance['AMT_DRAWINGS_OTHER_CURRENT'] + credit_card_balance[
                                              'AMT_DRAWINGS_POS_CURRENT']
    credit_card_balance['CNT_DRAWINGS'] = credit_card_balance['CNT_DRAWINGS_ATM_CURRENT'] + credit_card_balance[
        'CNT_DRAWINGS_CURRENT'] + credit_card_balance['CNT_DRAWINGS_OTHER_CURRENT'] + credit_card_balance[
                                              'CNT_DRAWINGS_POS_CURRENT']
    credit_card_balance_sorted = pd.DataFrame()
    credit_card_balance_sorted = credit_card_balance.groupby('SK_ID_PREV').max('MONTHS_BALANCE')[['SK_ID_CURR']]
    credit_card_balance_sorted['AVG_AMT_BALANCE'] = credit_card_balance.groupby('SK_ID_PREV')['AMT_BALANCE'].sum() / \
                                                    credit_card_balance.groupby('SK_ID_PREV')['AMT_BALANCE'].count()
    credit_card_balance_sorted['CREDIT_COUNT_ACTIVE'] = \
    credit_card_balance[credit_card_balance['NAME_CONTRACT_STATUS'] == 'Active'].groupby('SK_ID_PREV')[
        'NAME_CONTRACT_STATUS'].count()
    credit_card_balance_ID_CURR = credit_card_balance_sorted.groupby('SK_ID_CURR').sum()
    master_test = master_test.merge(credit_card_balance_ID_CURR, on='SK_ID_CURR', how='left')
    del (credit_card_balance)
    del (credit_card_balance_sorted)
    del (credit_card_balance_ID_CURR)

    installments_payments = pd.read_csv('installments_payments.csv')
    installments_payments['DIFF_DAY_PAYMENT'] = installments_payments['DAYS_ENTRY_PAYMENT'] - installments_payments[
        'DAYS_INSTALMENT']
    installments_payments['DIFF_AMT_PAYMENT'] = installments_payments['AMT_INSTALMENT'] - installments_payments[
        'AMT_PAYMENT']
    installments_payments_sorted = pd.DataFrame()
    installments_payments_sorted = installments_payments.groupby('SK_ID_PREV').max('MONTHS_BALANCE')[['SK_ID_CURR']]
    installments_payments_sorted['OCCURENCES'] = installments_payments.groupby('SK_ID_PREV').count()[
        'NUM_INSTALMENT_VERSION']
    installments_payments_sorted['SUM_DIFF_DAY_PAYMENT'] = installments_payments.groupby('SK_ID_PREV')[
        'DIFF_DAY_PAYMENT'].sum()
    installments_payments_sorted['AVG_DIFF_DAY_PAYMENT'] = installments_payments_sorted['SUM_DIFF_DAY_PAYMENT'] / \
                                                           installments_payments_sorted['OCCURENCES']
    installments_payments_sorted['SUM_DIFF_AMT_PAYMENT'] = installments_payments.groupby('SK_ID_PREV')[
        'DIFF_AMT_PAYMENT'].sum()
    installments_payments_sorted['AVG_DIFF_AMT_PAYMENT'] = installments_payments_sorted['SUM_DIFF_AMT_PAYMENT'] / \
                                                           installments_payments_sorted['OCCURENCES']
    installments_payments_sorted = installments_payments_sorted.drop(
        ['OCCURENCES', 'SUM_DIFF_DAY_PAYMENT', 'SUM_DIFF_AMT_PAYMENT'], axis=1)
    installments_payments_ID_CURR = installments_payments_sorted.groupby('SK_ID_CURR').sum()
    master_test = master_test.merge(installments_payments_ID_CURR, on='SK_ID_CURR', how='left')
    del (installments_payments)
    del (installments_payments_sorted)
    del (installments_payments_ID_CURR)

    previous_application = pd.read_csv('previous_application.csv')
    previous_application_sorted = pd.DataFrame()
    previous_application_sorted['COUNT_LOANS'] = previous_application.groupby('SK_ID_CURR')['SK_ID_PREV'].nunique()
    previous_application_sorted['COUNT_REVOLVING'] = \
    previous_application[previous_application['NAME_CONTRACT_TYPE'] == 'Revolving loans'].groupby('SK_ID_CURR')[
        'NAME_CONTRACT_TYPE'].count()
    previous_application_sorted['SUM_AMT_ANNUITY'] = previous_application.groupby('SK_ID_CURR')['AMT_ANNUITY'].sum()
    previous_application_sorted['AVG_AMT_ANNUITY'] = previous_application_sorted['SUM_AMT_ANNUITY'] / \
                                                     previous_application_sorted['COUNT_LOANS']
    previous_application_sorted['SUM_AMT_APPLICATION'] = previous_application.groupby('SK_ID_CURR')[
        'AMT_APPLICATION'].sum()
    previous_application_sorted['AVG_AMT_APPLICATION'] = previous_application_sorted['SUM_AMT_APPLICATION'] / \
                                                         previous_application_sorted['COUNT_LOANS']
    previous_application_sorted['AVG_DAYS_DECISION'] = previous_application.groupby('SK_ID_CURR')[
                                                           'DAYS_DECISION'].sum() / \
                                                       previous_application.groupby('SK_ID_CURR')[
                                                           'DAYS_DECISION'].count()
    previous_application_sorted['COUNT_REJECT'] = \
    previous_application[previous_application['CODE_REJECT_REASON'] != 'XAP'].groupby('SK_ID_CURR')[
        'CODE_REJECT_REASON'].count()
    previous_application_sorted[['COUNT_REVOLVING', 'COUNT_REJECT']] = previous_application_sorted[
        ['COUNT_REVOLVING', 'COUNT_REJECT']].fillna(0)
    master_test = master_test.merge(previous_application_sorted, on='SK_ID_CURR', how='left')
    del (previous_application)
    del (previous_application_sorted)

    index_test = master_test.iloc[:, 0]
    master_test = master_test.drop(['SK_ID_CURR'], axis=1)

    

    # test on different fill na methods
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    for i in master.columns:
        master[i] = imp.fit_transform(master[[i]])
    for i in master_test.columns:
        master_test[i] = imp.fit_transform(master_test[[i]])
    '''
    master = master.fillna(0)
    master_test = master_test.fillna(0)
    '''

    # scale data
    X = preprocessing.MinMaxScaler().fit_transform(master.iloc[:, 1:])
    y = master.iloc[:, 0]
    x_test = preprocessing.MinMaxScaler().fit_transform(master_test)

    
    #x_train, x_val, y_train, y_val = train_test_split(master.iloc[:, 1:], master.iloc[:, 0], test_size=0.2, random_state=42)


    log_reg = LogisticRegression(max_iter=5000, C=0.01 ,class_weight='balanced')
    #log_reg = LogisticRegression(max_iter=5000)

    # use cross validation for hyperparameters
    cv = StratifiedKFold()
    # scores = cross_val_score(log_reg, X, y, scoring='roc_auc', cv=cv, n_jobs=-1)
    # print(mean(scores))
    # plain comparison

    # export results to csv
    log_reg.fit(X, y)
    y_pred_pro = log_reg.predict_proba(x_test)[:, 1]
    # write to csv
    with open('output.csv', 'w', encoding="gbk", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['SK_ID_CURR', 'TARGET'])
        for i in range(len(index_test)):
            csv_writer.writerow([index_test[i], round(y_pred_pro[i], 1)])

    

    # run grid search for hyperparameters
    '''
    from sklearn.model_selection import GridSearchCV
    penalty =['none', 'l2'] 
    c_values = [100, 10, 1.0, 0.1, 0.01]
    class_weight = ['balanced', None]
    model = LogisticRegression(max_iter=5000)
    param_ne = dict(class_weight=class_weight, C=c_values, penalty=penalty)
    gsearch = GridSearchCV(model, param_grid=param_ne, scoring='roc_auc', cv=cv)
    gsearch.fit(X, y)
    means = gsearch.cv_results_['mean_test_score']
    params = gsearch.cv_results_['params']

    print(gsearch.best_params_, gsearch.best_score_)
    for mean, param in zip(means, params):
        print("%f with: %r" % (mean, param))     
    '''    

    

    
