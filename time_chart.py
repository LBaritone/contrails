# Iterate through with setup from predict.py
# Make each day a bin
# Accumulate data for many bins
# 	For each valid line (in a bin), call predict_line_py
# 	Count predicted contrails for bin and corresponding data
# 
# Plot line on x-y axes where time is x for the time for data readings
# 						and y is number of predicted contrail formations
# predicted: list
# days/bins: list
# plot line graph 

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot
import numpy as np
import re
import plotly.offline as offline
import plotly.graph_objs as go
from predict_line import *

days = []
count_per_day = []
local_count = 0

# target height for airplanes in meters
target = 11300
margin = 1000
close_lines = np.array([[0.] * 13])

with open("data/2017orderedweather87418.txt", "r") as infile:
# with open("data/weather.txt", "r") as infile:
	# get the station number from the first line 
	firstline = infile.readline().split()
	first_len = len(firstline)
	station = firstline[0]
	cur_date = " ".join(firstline[-3:])
	for line in infile:
		data = line.split()

		# if is a new bock of data (new day or new time on a day)
		if (len(data) == first_len and data[0] == station) :
			next = 0
			# if you see data for a new day here then add a new bin
			if (" ".join(data[-3:]) != cur_date) :
				days.append(" ".join(data[-3:]))
				count_per_day.append(local_count)
				cur_date = " ".join(data[-3:])
				local_count = 0
			
		# if the line is a data line
		# (not re.search('[^\.0-9]', data[0])) only returns True when 
   		# data[0] contains only digits and "."s
		if (len(data) > 10) and \
			(not data[0].startswith('--')) and \
		   	(not data[0].startswith('PRES')) and \
		   	(not data[0].startswith('hPa')) and \
		   	(not re.search('[^\.0-9]', data[0])) and \
		   	(not re.search('[^\.0-9]', data[1])) :

		   	# Only test a single data height closest to the target
		   	height = float(data[1])
		   	if margin >= abs(target - height) :
		   		line = np.array(data).astype(np.float)
		   		line = np.lib.pad(line, (0, 13 - len(line)), "constant", constant_values=(0, 0))    
		   		close_lines = np.vstack([close_lines, line])
		   	elif margin < abs(target - height) and (height > target) and next == 0 :

		   		# find row with height closest to target
		   		if close_lines.shape[0] > 1 :
		   			closest = close_lines[np.abs(close_lines[:,1] - target).argmin()]
		   		else :
		   			closest = close_lines[np.abs(close_lines[0][1] - target).argmin()]

			   	# find way to make a new bin
			   	pred = predict_line(closest)
			   	local_count += 1 if pred else 0
			   	next = 1
			   	close_lines = np.array([[0.] * 13])



offline.plot({'data': [{'x': days, 'y': count_per_day}], 
               'layout': {'title': 'Contrail Predictions for all Readings a Day for 2017 (Mendoza)', 
                          'font': dict(size = 16),
                          'xaxis': dict(title = "Time"),
                          'yaxis': dict(title = 'Number of Contrail Predictions')}},
             image='png')

print len(days)


