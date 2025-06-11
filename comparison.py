import pandas as pd
import numpy as np
import openpyxl


def get_data(path):

    specific_subj = pd.read_excel(path, sheet_name="Поручения отдельным субъектам").fillna(0)
    all_subj =  pd.read_excel(path, sheet_name="Поручения субъектам").fillna(0)

    all_subj = all_subj.rename(columns= lambda x: x.strip(' '))
    codes_all_subj = all_subj[['Для кого','Номер']]
    codes = dict(zip(codes_all_subj['Номер'].tolist(), codes_all_subj['Для кого'].tolist()))

    specific_subj = specific_subj.rename(columns= lambda x: x.strip(' '))
    specific_subj = specific_subj[['Субъект РФ','ОКТМО']]
    spec_subject = dict(zip(specific_subj['Субъект РФ'].tolist(), specific_subj['ОКТМО'].tolist()))

    d = {}
    for region, code in spec_subject.items():
        nums = []
        for k, v in codes.items():
            if code == v:
                nums.append(k)
        d.update({region:nums})


    no_data = {}
    data = {}
    for reg, num in d.items():
        if len(num)!=0:
            data.update({reg:', '.join(num)})
        else:
            no_data.update({reg:'---'})


    return data, no_data