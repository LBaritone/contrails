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
close_lines = np.array([])

with open("data/2017orderedweather87418.txt", "r") as infile:
# with open("data/weather.txt", "r") as infile:
	# get the station number from the first line 
	firstline = infile.readline().split()
	first_len = len(firstline)
	station = firstline[0]
	for line in infile:
		data = line.split()

		# if you see data for a new day or time on a day here then add a new bin
		if (len(data) == first_len and data[0] == station) :
			days.append(" ".join(data[-4:]))
			count_per_day.append(local_count)
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
		   	if margin > abs(target - height) :
		   		print 'foo'
		   		print data
		   		np.append(close_lines, np.array(data))
		   	elif margin < abs(target - height) and (height > target) :

		   		# find row with height closest to target
		   		print height
		   		print target
		   		print close_lines
		   		print np.abs(close_lines[:,1] - target)
		   		closest = close_lines[np.abs(close_lines[:,1] - target).argmin()]

		   		print closest

			   	# find way to make a new bin
			   	pred = predict_line(closest)
			   	local_count += 1 if pred else 0

# offline.plot({'data': [{'x': days, 'y': count_per_day}], 
#                'layout': {'title': 'Contrail Predictions for all Readings a Day for 2017 (Mendoza)', 
#                           'font': dict(size = 16),
#                           'xaxis': dict(title = "Time"),
#                           'yaxis': dict(title = 'Number of Contrail Predictions')}},
#              image='png')





