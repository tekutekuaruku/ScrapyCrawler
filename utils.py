import os
import pandas as pd
import csv

def makeDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def excel_to_csv(path):
    #Read excel
    data = pd.read_excel(path, engine='openpyxl',index_col=None)
    #Convert from excel to csv
    output_path = path.replace("xlsx", "csv")
    data.to_csv(output_path, encoding='utf-8', index=False)
    os.remove(path)
    return output_path

def csv_to_dict(path):
    dictionary = []
    with open(path, 'r',encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dictionary.append(row)
        return dictionary
