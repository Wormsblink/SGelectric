import os
import pandas as pd
import zipfile

def merge_csv(folder_name,output_file_name):
	filepaths = get_filepaths("/" + folder_name)

	compiled_df = pd.DataFrame()

	for filepath in filepaths:
		if filepath.endswith('.zip'):
			with zipfile.ZipFile(filepath) as zf:
				for filename in zf.namelist():
					zipped_file_names = zf.getinfo(filename)
					with zf.open(filename, 'r') as csv_file:
						df = pd.read_csv(csv_file)

						compiled_df = compiled_df._append(df)

	compiled_df.to_csv(output_file_name)

	return (output_file_name)


def get_filepaths(folder_name):
	filepaths = []
	current_dir = os.getcwd()
	folder_dir = current_dir + folder_name
	files_list = os.listdir (folder_dir)

	for file in files_list:
		filepaths.append(os.path.join(folder_dir,file))
	
	return filepaths

#merge_csv("USEP Data","Compiled USEP Data.csv")