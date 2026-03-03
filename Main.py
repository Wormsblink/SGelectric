import merge
import pandas as pd
from datetime import datetime

import matplotlib
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

#temp
import time

#Settings
USEP_Folder = "USEP Data"
USEP_Compiled_File = "Compiled USEP Data.csv"

#plt.rcParams.update({'font.size': 16})
#plt.rcParams['figure.figsize'] = 12.5, 7

def main():
	merge.merge_csv(USEP_Folder, USEP_Compiled_File)

	df = pd.read_csv(USEP_Compiled_File, usecols=["DATE","USEP ($/MWh)", "DEMAND (MW)"])
	df = add_daily_average(df, "USEP ($/MWh)","DAILY USEP ($/MWh)")

	#df.to_csv("test.csv")

	animated_gif = create_image(df, "DATE", "DAILY USEP ($/MWh)","DEMAND (MW)")
	animated_gif.show()

def add_daily_average(df, target_col, new_col_name):
	df[new_col_name] = df[target_col].rolling(48).mean()
	df = df.iloc[24::48, :]
	return df

def create_image(df, date_col_name, *args):

	fig = plt.figure()
	plt.xlabel(date_col_name)
	fig.get_axes()[0].set_axis_off()

	x = get_dates_list(df, "DATE")

	for row_pos,dataset in enumerate(args):
		newline = df[dataset].values.tolist()
	
		ax = fig.add_subplot(len(args),1,row_pos+1, sharex = fig.get_axes()[0])
		ax.plot(x, newline, label = dataset)
		ax.legend(loc = 'upper right')
	
	plt.tight_layout()

	return plt

def get_dates_list(df, date_col_name):
	raw_dates = df[date_col_name].values.tolist()

	parsed_dates = []

	for date in raw_dates:
		parsed_dates.append(datetime.strptime(date,"%Y-%m-%d"))
	return parsed_dates

main()			