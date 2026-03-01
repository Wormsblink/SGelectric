import merge
import pandas as pd
from datetime import datetime
from bokeh.plotting import figure, show

#Settings
USEP_Folder = "USEP Data"
USEP_Compiled_File = "Compiled USEP Data.csv"

merge.merge_csv(USEP_Folder, USEP_Compiled_File)

df = pd.read_csv(USEP_Compiled_File)

x = []
raw_dates = df['DATE'].values.tolist()

for date in raw_dates:
	x.append(datetime.strptime(date,"%Y-%m-%d"))

y1 = df['USEP ($/MWh)'].values.tolist()

plot = figure (title = "USEP over time", x_axis_label = "Date", x_axis_type ='datetime', y_axis_label = "($/MWh)")

plot.line(x, y1, legend_label="USEP", line_width=2)

show(plot)