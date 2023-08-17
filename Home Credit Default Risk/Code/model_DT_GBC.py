'''
Feature selection / engineering on csv files
Prepare test file
Decision Trees, GradientBoosting, Random Forest
5 fold cross validation used for fitting
Hyper-parameter Tuning
'''
import pandas as pd
import numpy as np
from sklearn import tree, preprocessing
import csv

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc, roc_curve, roc_auc_score, RocCurveDisplay
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, cross_val_score
from statistics import mean


def plot_roc_curve(y, prob, est_name):
    fpr, tpr, threshold = roc_curve(y, prob)
    roc_auc = auc(fpr, tpr)
    display = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name=est_name)
    display.plot()
    plt.show()


def plot_multi_models_roc(names, sampling_methods, colors, x_tests, y_tests):
    plt.figure(figsize=(20, 20), dpi=100)
    # auc_string = ['0.74219', '0.76266']
    for (name, method, colorname, x_test, y_test) in zip(names, sampling_methods, colors, x_tests, y_tests):
        y_test_predprob = method.predict_proba(x_test)[:, 1]
        fpr, tpr, thresholds = roc_curve(y_test, y_test_predprob, pos_label=1)
        plt.plot(fpr, tpr, lw=5, label='{} (AUC={:.2f})'.format(name, auc(fpr, tpr)), color=colorname)
        plt.axis('square')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.xlabel('False Positive Rate', fontsize=20)
        plt.ylabel('True Positive Rate', fontsize=20)
        plt.title('ROC Curve', fontsize=25)
        plt.legend(loc='lower right', fontsize=20)
    plt.plot([0, 1], [0, 1], '--', lw=5, color='grey')
    plt.savefig('multi_models_roc.png')
    return plt


if __name__ == '__main__':

    application_train = pd.read_csv('application_train.csv')

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
    # print(master)




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

    # master = master.fillna(0)
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    for i in master.columns:
        master[i] = imp.fit_transform(master[[i]])
    for i in master_test.columns:
        master_test[i] = imp.fit_transform(master_test[[i]])

    # x_train, x_test, y_train, y_test = train_test_split(master.iloc[:, 1:], master.iloc[:, 0], test_size=0.2, random_state=42)
    # x_train_mm = preprocessing.MinMaxScaler().fit_transform(x_train)
    # x_test_mm = preprocessing.MinMaxScaler().fit_transform(x_test)
    x_train_all, y_train_all = master.iloc[:, 1:], master.iloc[:, 0]
    x_test = master_test

    # Decision Tree
    # clf = tree.DecisionTreeClassifier(min_samples_leaf=0.02, criterion='entropy', random_state=10)
    # clf = tree.DecisionTreeClassifier(criterion='entropy', random_state=10)
    # cv = StratifiedKFold()
    # scores = cross_val_score(estimator=clf, X=x_train_all, y=y_train_all, scoring='roc_auc', cv=cv, n_jobs=-1)
    # print(f'AUC Score (Train Data): {mean(scores)}')
    # plot_roc_curve(y_test, model.predict_proba(x_test_rb)[:, 1], 'Decision Tree')
    # AUC Score (Train Data): 0.5420485227170853 0
    # AUC Score (Train Data): 0.5447555142629571 mean
    # AUC Score (Train Data): 0.5427053035745981 median
    # AUC Score (Train Data): 0.5419071930078075 most_frequent

    # GradientBoosting
    # gbc = GradientBoostingClassifier()
    # cv = StratifiedKFold()
    # scores = cross_val_score(estimator=gbc, X=x_train_all, y=y_train_all, scoring='roc_auc', cv=cv, n_jobs=-1)
    # print(f'AUC Score (Train Data): {mean(scores)}')
    # AUC Score (Train Data): 0.7541658918106675 for 0
    # AUC Score (Train Data): 0.7546770211451014 for mean
    # AUC Score (Train Data): 0.7546917662325033 for median
    # AUC Score (Train Data): 0.7553556695509099 for most_frequent

    # Random Forest
    # rfc = RandomForestClassifier()
    # cv = StratifiedKFold()
    # scores = cross_val_score(estimator=rfc, X=x_train_all, y=y_train_all, scoring='roc_auc', cv=cv, n_jobs=-1)
    # print(f'AUC Score (Train Data): {mean(scores)}')
    # AUC Score (Train Data): 0.7274407021379657 for 0
    # AUC Score (Train Data): 0.7289112248999184 for mean
    # AUC Score (Train Data): 0.7286512301145306 for median
    # AUC Score (Train Data): 0.7303926726483275 for most_frequent

    # GradientBoosting with best params
    gbc = GradientBoostingClassifier(learning_rate=0.2, min_samples_leaf=0.02, n_estimators=300)
    model = gbc.fit(x_train_all, y_train_all)
    # y_pred = model.predict(x_test)
    
    y_pred_pro = model.predict_proba(x_test)[:, 1]
    # write to csv
    with open('output.csv', 'w', encoding="gbk", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['SK_ID_CURR', 'TARGET'])
        for i in range(len(index_test)):
            csv_writer.writerow([index_test[i], round(y_pred_pro[i], 1)])

    # print("AUC Score (Train):", roc_auc_score(y_test, model.predict_proba(x_test)[:, 1]))
    # plot_roc_curve(y_test, model.predict_proba(x_test)[:, 1], 'Gradient Boosting Decision Tree')
    # AUC Score (Train): 0.7621254888771649 for 0
    # AUC Score (Train): 0.7615058789024576 for mean
    # AUC Score (Train): 0.7618407977089336 for median
    # AUC Score (Train): 0.7630704137394694 for most_frequent

    # search the params
    # param_ne = {'learning_rate': [0.1, 0.2, 0.3], 'min_samples_leaf': [0.01, 0.02, 0.03], 'n_estimators': [100, 200, 300]}
    # # learning_rate=0.3, min_samples_leaf=0.02, n_estimators=90
    # gsearch = GridSearchCV(estimator=GradientBoostingClassifier(random_state=10),  param_grid=param_ne, scoring='roc_auc', n_jobs=-1)
    # gsearch.fit(x_train_all, y_train_all)
    # # cv = KFold(n_splits=5, random_state=1, shuffle=True)
    # # scores = cross_val_score(estimator=gbc, X=x_train_all, y=y_train_all, scoring='roc_auc', cv=cv, n_jobs=-1)
    # print(f'The best params is: {gsearch.best_params_} and the best score is: {gsearch.best_score_}')
    # means = gsearch.cv_results_['mean_test_score']
    # params = gsearch.cv_results_['params']
    # for mean, param in zip(means, params):
    #     print("%f  with:   %r" % (mean, param))

    # plot the best models
    # log_reg = LogisticRegression(max_iter=5000, penalty='none', class_weight='balanced')
    # model_log_reg = log_reg.fit(x_train_mm, y_train)
    # gbc = GradientBoostingClassifier(learning_rate=0.2, min_samples_leaf=0.02, n_estimators=300)
    # model_gbc = gbc.fit(x_train, y_train)
    # names = ['Logistic Regression', 'Gradient Boosting Classifier']
    # models = [log_reg, gbc]
    # colors = ['red', 'blue']
    # x_tests = [x_test_mm, x_test]
    # y_tests = [y_test, y_test]
    # plot_multi_models_roc(names, models, colors, x_tests, y_tests)


    """
TThe best params is: {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 90} and the best score is: 0.7596202640536307
0.751257  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 60}
0.752789  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 70}
0.754068  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 80}
0.755084  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 90}
0.750757  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 60}
0.752383  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 70}
0.753695  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 80}
0.754696  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 90}
0.750664  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 60}
0.752366  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 70}
0.753526  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 80}
0.754526  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 90}
0.749898  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.04, 'n_estimators': 60}
0.751580  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.04, 'n_estimators': 70}
0.752792  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.04, 'n_estimators': 80}
0.753794  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.04, 'n_estimators': 90}
0.755913  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.01, 'n_estimators': 60}
0.757058  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.01, 'n_estimators': 70}
0.757872  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.01, 'n_estimators': 80}
0.758382  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.01, 'n_estimators': 90}
0.756246  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 60}
0.757234  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 70}
0.757976  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 80}
0.758689  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 90}
0.755625  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.03, 'n_estimators': 60}
0.756759  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.03, 'n_estimators': 70}
0.757582  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.03, 'n_estimators': 80}
0.758257  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.03, 'n_estimators': 90}
0.755690  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.04, 'n_estimators': 60}
0.756669  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.04, 'n_estimators': 70}
0.757386  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.04, 'n_estimators': 80}
0.757995  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.04, 'n_estimators': 90}
0.757420  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 60}
0.758488  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 70}
0.759052  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 80}
0.759407  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 90}
0.757597  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 60}
0.758563  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 70}
0.759200  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 80}
0.759620  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 90}
0.757633  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 60}
0.758510  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 70}
0.759001  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 80}
0.759490  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 90}
0.756393  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.04, 'n_estimators': 60}
0.756948  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.04, 'n_estimators': 70}
0.757692  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.04, 'n_estimators': 80}
0.758190  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.04, 'n_estimators': 90}
0.757971  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.01, 'n_estimators': 60}
0.758650  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.01, 'n_estimators': 70}
0.759105  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.01, 'n_estimators': 80}
0.759549  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.01, 'n_estimators': 90}
0.757600  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.02, 'n_estimators': 60}
0.758169  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.02, 'n_estimators': 70}
0.758530  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.02, 'n_estimators': 80}
0.758711  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.02, 'n_estimators': 90}
0.757593  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.03, 'n_estimators': 60}
0.757979  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.03, 'n_estimators': 70}
0.758407  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.03, 'n_estimators': 80}
0.758766  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.03, 'n_estimators': 90}
0.756481  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.04, 'n_estimators': 60}
0.757195  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.04, 'n_estimators': 70}
0.757790  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.04, 'n_estimators': 80}
0.758317  with:   {'learning_rate': 0.4, 'min_samples_leaf': 0.04, 'n_estimators': 90}
    """

"""
    The best params is: {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 110} and the best score is: 0.7604208740774385
0.752789  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 70}
0.755084  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 90}
0.756642  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 110}
0.752383  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 70}
0.754696  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 90}
0.756184  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 110}
0.752366  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 70}
0.754526  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 90}
0.756042  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 110}
0.758488  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 70}
0.759407  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 90}
0.760236  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 110}
0.758563  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 70}
0.759620  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 90}
0.760421  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 110}
0.758510  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 70}
0.759490  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 90}
0.760190  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 110}
0.757719  with:   {'learning_rate': 0.5, 'min_samples_leaf': 0.01, 'n_estimators': 70}
0.758602  with:   {'learning_rate': 0.5, 'min_samples_leaf': 0.01, 'n_estimators': 90}
0.758584  with:   {'learning_rate': 0.5, 'min_samples_leaf': 0.01, 'n_estimators': 110}
0.757797  with:   {'learning_rate': 0.5, 'min_samples_leaf': 0.02, 'n_estimators': 70}
0.758436  with:   {'learning_rate': 0.5, 'min_samples_leaf': 0.02, 'n_estimators': 90}
0.758920  with:   {'learning_rate': 0.5, 'min_samples_leaf': 0.02, 'n_estimators': 110}
0.757371  with:   {'learning_rate': 0.5, 'min_samples_leaf': 0.03, 'n_estimators': 70}
0.757885  with:   {'learning_rate': 0.5, 'min_samples_leaf': 0.03, 'n_estimators': 90}
0.758282  with:   {'learning_rate': 0.5, 'min_samples_leaf': 0.03, 'n_estimators': 110}
"""

"""
The best params is: {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 300} and the best score is: 0.7626617790970294
0.755258  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 100}
0.759917  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 200}
0.761600  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 300}
0.755177  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 100}
0.759925  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 200}
0.761816  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 300}
0.754564  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 100}
0.759419  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 200}
0.761259  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 300}
0.759128  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.01, 'n_estimators': 100}
0.761660  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.01, 'n_estimators': 200}
0.762182  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.01, 'n_estimators': 300}
0.759017  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 100}
0.761881  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 200}
0.762662  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 300}
0.758599  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.03, 'n_estimators': 100}
0.761584  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.03, 'n_estimators': 200}
0.762287  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.03, 'n_estimators': 300}
0.760536  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 100}
0.761396  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 200}
0.761330  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 300}
0.759980  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 100}
0.761437  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 200}
0.761594  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 300}
0.759254  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 100}
0.760751  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 200}
0.761081  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 300}
"""
"""
The best params is: {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 300} and the best score is: 0.7626617790970294
0.755258  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 100}
0.759917  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 200}
0.761600  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.01, 'n_estimators': 300}
0.755177  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 100}
0.759925  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 200}
0.761816  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.02, 'n_estimators': 300}
0.754564  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 100}
0.759419  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 200}
0.761259  with:   {'learning_rate': 0.1, 'min_samples_leaf': 0.03, 'n_estimators': 300}
0.759128  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.01, 'n_estimators': 100}
0.761660  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.01, 'n_estimators': 200}
0.762182  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.01, 'n_estimators': 300}
0.759017  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 100}
0.761881  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 200}
0.762662  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.02, 'n_estimators': 300}
0.758599  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.03, 'n_estimators': 100}
0.761584  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.03, 'n_estimators': 200}
0.762287  with:   {'learning_rate': 0.2, 'min_samples_leaf': 0.03, 'n_estimators': 300}
0.760536  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 100}
0.761396  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 200}
0.761330  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.01, 'n_estimators': 300}
0.759980  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 100}
0.761437  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 200}
0.761594  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.02, 'n_estimators': 300}
0.759254  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 100}
0.760751  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 200}
0.761081  with:   {'learning_rate': 0.3, 'min_samples_leaf': 0.03, 'n_estimators': 300}
"""