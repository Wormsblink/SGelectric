import matplotlib
from matplotlib import animation
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})
plt.rcParams['figure.figsize'] = 12.5, 7
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
from functools import cache

from datetime import datetime
import pandas as pd

df=pd.read_excel('alldays.xlsx', header = 0)


t = []
y1 = []
y2 = []
y3 = []
y4 = []

for index, row in df.iterrows():

    #t.append(datetime.strptime(row['DATE'],'%Y-%m-%d'))
    t.append(row['DATE'])
    y1.append(row['USEP ($/MWh)'])
    y2.append(row['DEMAND (MW)'])
    y3.append(row['AnnualAve'])
    y4.append(row['BRENT CRUDE'])

y2[:] = [x / 10 for x in y2]

fig, ((ax, ax2)) = plt.subplots(2,sharex=True)


line2, = ax.plot(t, y2, color = "g", label = 'Average Energy Demand (10s MW)', linewidth=2)
line1, = ax.plot(t, y1, color = "r", label = 'Uniform Singapore Energy Price ($/MWh)', linewidth=2)
line3, = ax.plot(t, y3, color = "b", label = 'Annual Average Energy Price ($/MWh)', linewidth=2)
line4, = ax2.plot(t, y4, color = 'black', label = 'BRENT CRUDE (USD/BBL)', linewidth=2)

def update(num,t,y1,y2,line1,line2):

    if(num<366):
        plt.xlim(min(t), t[num])
        ax.set_ylim(0, 1000)
        line1.set_data(t[0:num], y1[0:num])
        line2.set_data(t[0:num], y2[0:num])

        while(len(ax.texts)>0):
            del(ax.texts[-1])
        while(len(ax2.texts)>0):
            del(ax2.texts[-1])
        ax.text(t[num], 0, t[num].strftime("%d %b %y") + "\n $" + str(round(y1[num],2)), fontsize=18, color = "r")
        ax.text(t[num], 250, "\n\n" + str(round(y2[num]*10)) + " MW", fontsize=16, color = "g")
        ax2.text(t[num], y4[num], t[num].strftime("%d %b %y") + "\n $" + str(round(y4[num],2)), fontsize=18, color = "black")

    else:
        line1.set_data(t[num-365:num], y1[num-365:num])
        line2.set_data(t[num-365:num], y2[num-365:num])
        plt.xlim(t[num-365], t[num])
        ax.set_ylim(0, 1000)
        while(len(ax.texts)>0):
            del(ax.texts[-1])
        while(len(ax2.texts)>0):
            del(ax2.texts[-1])
        ax.text(t[num], 0, t[num].strftime("%d %b %y") + "\n $" + str(round(y1[num],2)), fontsize=18, color = "r") 
        ax.text(t[num], 250, "\n\n" + str(round(y2[num]*10)) + " MW", fontsize=16, color = "g")
        ax2.text(t[num], y4[num], t[num].strftime("%d %b %y") + "\n $" + str(round(y4[num],2)), fontsize=18, color = "black")

    return [line1,line2]

ani = animation.FuncAnimation(fig, update, len(t), fargs=[t, y1, y2, line1, line2],
                  interval=1,repeat = False)

fig.autofmt_xdate()

ax.legend(loc = 'upper right')
ax2.legend(loc = 'upper right')

plt.minorticks_on()

ax.set_ylabel('Daily Averaged \nElectricity Price ($/MWh)')
ax2.set_ylabel('Brent Crude Price \nUSD/BBL')
plt.xlabel('Dates')
plt.grid(which = 'major')

#ani.save("Wholesale_Electricity_Price.gif", fps=15)      
#Toggle above line if you want to display gif in real-time as it is being rendered

plt.show()