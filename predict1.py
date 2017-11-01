#
# Takes input variables (ambient pressure and RH) from xxx
# calls fortran script to determine RHI Tls for formation of 
# contrial 
import numpy as np
# import calc.f90




with open('in.txt', 'r') as infile:
    for line in infile:
    	data = line.replace(',', ' ').split()
    	p = float(data[0])
    	rh = float(data[1])
    	# print p
    	# print rh
    	C = calc.thres(pamb = p, rhamb = rh)
    	print C 
