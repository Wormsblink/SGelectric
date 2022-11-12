import os
from time import sleep
import pandas as pd
cwd = os.path.abspath('') 
files = os.listdir(cwd) 

if os.path.isfile('alldays.csv'):
	os.remove('alldays.csv')
else:
	print('alldays.csv not found')

sleep(0.4)

df = pd.DataFrame()
df2 = pd.DataFrame()
for file in files:
		if file.endswith('.csv'):
				print("Reading next csv file")
				df = df.append(pd.read_csv(file)) 
		if file.endswith('.xlsx'):
				print("Reading next xlsx file")
				df2 = df2.append(pd.read_excel(file))

df = df[['DATE','PERIOD','USEP ($/MWh)','DEMAND (MW)']]

df["DATE"] = pd.to_datetime(df["DATE"])
df2["DATE"]=pd.to_datetime(df2["DATE"])

df = df.groupby(['DATE']).mean()

df.sort_values('DATE',inplace=True)
df.reset_index(drop=False, inplace=True)

df = df[['DATE','USEP ($/MWh)', 'DEMAND (MW)']]

df.reset_index(drop=True, inplace=True)

df2.set_index('DATE')

df['AnnualAve'] = df['USEP ($/MWh)'].rolling(365).mean()

df = pd.merge(df,df2, how='outer')

print(df.head())

df.to_csv('alldays.csv')