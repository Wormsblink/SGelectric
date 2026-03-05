import os
import pandas as pd
import numpy as np
import zipfile
from datetime import datetime

def USEP_merge_csv(folder_name,output_file_name):
	filepaths = get_filepaths("/" + folder_name)

	compiled_df = pd.DataFrame()

	for filepath in filepaths:
		if filepath.endswith('.zip'):
			with zipfile.ZipFile(filepath) as zf:
				for filename in zf.namelist():
					zipped_file_names = zf.getinfo(filename)
					with zf.open(filename, 'r') as csv_file:
						df = pd.read_csv(csv_file)

						compiled_df = compiled_df._append(df, ignore_index = True)

	compiled_df["DATE"] = pd.to_datetime(compiled_df["DATE"].apply(parse_date))

	compiled_df = compiled_df.sort_values(by=["DATE","PERIOD"])
	compiled_df.to_csv(output_file_name)

	return (output_file_name)

def BRENT_merge_csv(folder_name,output_file_name):
	filepaths = get_filepaths("/" + folder_name)

	compiled_df = pd.DataFrame()

	for filepath in filepaths:
		df = pd.read_csv(filepath)
		compiled_df = compiled_df._append(df, ignore_index = True)

	compiled_df["observation_date"] = pd.to_datetime(compiled_df["observation_date"].apply(parse_date))
	compiled_df = compiled_df.replace('',np.nan).ffill()

	compiled_df = compiled_df.sort_values(by="observation_date")
	compiled_df.to_csv(output_file_name)

	return(output_file_name)

def get_filepaths(folder_name):
	filepaths = []
	current_dir = os.getcwd()
	folder_dir = current_dir + folder_name
	files_list = os.listdir (folder_dir)

	for file in files_list:
		filepaths.append(os.path.join(folder_dir,file))
	
	return filepaths

def parse_date(datestring):
	try:
		parsed_date = datetime.strptime(datestring,"%d %b %Y")
	except:
		try:
			parsed_date = datetime.strptime(datestring,"%d-%b-%Y")
		except:
			parsed_date = datetime.strptime(datestring,"%d/%m/%Y")

	return (parsed_date)

#USEP_merge_csv("USEP Data","Compiled USEP Data.csv")
#BRENT_merge_csv("Oil Data", "Compiled BRENT Data.csv")