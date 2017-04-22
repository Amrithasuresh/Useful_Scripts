#sample files dataset1.xlsx and dataset2.xlsx are provided
#BTW pandas are fantastic

import pandas as pd

#Writing in excel
from pandas import ExcelWriter

# Write to the file name
writer = ExcelWriter('common_dataset.xlsx')

#read files
x1 = pd.ExcelFile("dataset1.xlsx")
x2 = pd.ExcelFile("dataset2.xlsx")

#read the specific sheet
df1 = x1.parse("Sheet1")
df2 = x2.parse("Sheet1")

#merge the column "Featurenum"
merged = pd.merge(df1,df2, on="FeatureNum", how="inner")
merged.to_excel(writer,'Sheet1')
writer.save()

print(merged)
