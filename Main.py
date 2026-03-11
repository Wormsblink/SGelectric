import merge

import pandas as pd
import numpy as np
from datetime import datetime

from matplotlib.artist import Artist
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#temp
import time

#Settings
USEP_Folder = "USEP Data"
USEP_Compiled_File = "Compiled USEP Data.csv"

BRENT_Folder = "Oil Data"
BRENT_Compiled_File = "Compiled BRENT Data.csv"

#plt.rcParams.update({'font.size': 16})
plt.rcParams['figure.figsize'] = 14, 12

Averaging_Interval = 60

def main():
	merge.USEP_merge_csv(USEP_Folder, USEP_Compiled_File)
	merge.BRENT_merge_csv(BRENT_Folder, BRENT_Compiled_File)

	df = pd.read_csv(USEP_Compiled_File, usecols=["DATE","USEP ($/MWh)", "DEMAND (MW)"])
	

	df = add_rolling_average(df, "USEP ($/MWh)","DAILY AVERAGE USEP ($/MWh)", 48)
	df = add_rolling_average(df, "DEMAND (MW)", "DAILY POWER DEMAND (MW)", 48)
	df = df.iloc[24::48, :]

	df = add_rolling_average(df, "DAILY AVERAGE USEP ($/MWh)","28d Averaged USEP ($/MWh)",28)

	df2 = pd.read_csv(BRENT_Compiled_File)
	df = add_daily_value(df, df2,"DATE","observation_date")
	df = df.rename(columns={"DCOILBRENTEU":"BRENT CRUDE ($/BBL)"})

	df = add_rolling_average(df,"BRENT CRUDE ($/BBL)","28d Averaged Brent Crude ($/BBL)",28)

	df.to_csv("test.csv")

	create_animation(df, "DATE", "DAILY AVERAGE USEP ($/MWh)","BRENT CRUDE ($/BBL)","28d Averaged USEP ($/MWh)","28d Averaged Brent Crude ($/BBL)","DAILY POWER DEMAND (MW)")

def add_daily_value(df, df2, df_date_col, df2_date_col):
	df = df.join(df2.set_index(df2_date_col), on=df_date_col)
	df = df.replace('',np.nan).ffill()

	return df

def add_rolling_average(df, target_col, new_col_name, interval):
	df[new_col_name] = df[target_col].rolling(interval).mean()
	return df

def create_animation(df, date_col_name, *args):

	fig = plt.figure()
	
	plt.xlabel("Dates")
	fig.get_axes()[0].set_axis_off()
	
	dates_list = get_dates_list(df)

	for row_pos,dataset in enumerate(args):
		ax = fig.add_subplot(len(args),1,row_pos+1, sharex = fig.get_axes()[0], label = dataset)
		ax.set_title(dataset)

	ani = FuncAnimation(fig, create_image, len(df.index), fargs=[fig, df, dates_list, *args])
	
	fig.autofmt_xdate()
	#plt.show()
	ani.save("USEP_animated.gif", fps=30)

	return None

def create_image(end_frame, fig, df, dates_list, *args):

	newlines = ()
	start_frame = 0

	if end_frame>365:
		start_frame = end_frame-365

	for axes_pos,dataset in enumerate(args):
		
		target_axes = fig.get_axes()[axes_pos+1]

		for current_lines in list(target_axes.lines):
   			current_lines.remove()

		dataset_values = df[dataset].values.tolist()

		newline = (target_axes.plot(dates_list[start_frame:end_frame],dataset_values[start_frame:end_frame], color = "black"),)
		newlines = newlines + newline

		axes_min_x = dates_list[start_frame]
		axes_max_x = dates_list[end_frame+1]
		axes_min_y = get_min_value_dataset(df,dataset,start_frame,end_frame)*0.9
		axes_max_y = get_max_value_dataset(df,dataset,start_frame,end_frame)*1.1

		target_axes.set_xlim(axes_min_x,axes_max_x)
		target_axes.set_ylim(axes_min_y,axes_max_y)

		try:
			for text in target_axes.texts:
				Artist.remove(text)

			target_axes.text(dates_list[end_frame+1], (axes_max_y+axes_min_y)*0.5, dates_list[end_frame].strftime("%d %b %y") + ": \n" + str(round(dataset_values[end_frame],2)))
			
			try:
				percent_change = round((dataset_values[end_frame] - dataset_values[end_frame-Averaging_Interval])/(dataset_values[end_frame-Averaging_Interval])*100,1)
				
				if(end_frame<Averaging_Interval):
					pass
				else:
					target_axes.text(dates_list[end_frame+1], (axes_max_y+axes_min_y)*0.5-(axes_max_y-axes_min_y)*0.25, "Change (" + str(Averaging_Interval) + "d): \n" + str(percent_change) + "%")
			except:
				pass
		except:
			pass

	return None

def get_min_value_dataset(df,target_col, start, end):
	trunc_df = df[start:end][target_col]
	min_val = trunc_df.min()
	
	if np.isnan(min_val):
		min_val = 0
	else:
		pass

	return min_val

def get_max_value_dataset(df, target_col, start, end):
	trunc_df = df[start:end][target_col]
	max_val = trunc_df.max()
	
	if np.isnan(max_val):
		max_val = 1
	else:
		pass

	return max_val	
	
def get_dates_list(df):
	raw_dates = df["DATE"].values.tolist()

	parsed_dates = []

	for date in raw_dates:
		parsed_dates.append(datetime.strptime(date,"%Y-%m-%d"))
	return parsed_dates

main()			