import numpy as np

# Physical constants 
t0 = 273.16e0                # Absolute T
rd = 287.05e4                # Gas constant for dry air
rh2o = 461.5e4               # Gas constant for H2O
cp = 1.005e7                 # Specific heat capacity of air
bk = 1.381e-16               # Boltzman's constant
ba = 6.1115e0                # Constants for ice saturation density
bb = 23.036e0                # (Buck [J. Atmos. Sci., 20, 1527, 1981])
bc = 279.82e0
bd = 333.7
bal = 6.1121e0               # liquid saturation
bbl = 18.729e0
bcl = 257.87e0
bdl = 227.3e0

# Constants for saturation vapor pressure from Tabazadeh et al. [1997]
c1 = 18.452406985e0
c2 = -3505.1578807e0
c3 = -330918.55082e0
c4 = 12725068.262e0

delh = 42.e10                # Heat liberated per gram fuel
wexh = 1.25e0                # Water vapor mixing ratio in exhaust
effic = 0.3e0                # fraction of combustion heat converted to propulsion


def predict_line(data_line):
	pamb = float(data_line[0]) * 1.e3      # convert to bar
	tamb = float(data_line[2])
	if data_line[-1] :
		rhamb = float(data_line[5]) / 100.
	else :
		rhamb = float(data_line[4]) / 100.

	#  To find threshold temperature, begin at high ambient temperature and
	#  steadily decrease the temperature.  At each step, calculate the maximum
	#  plume relative humidity (with respect to water) [RH].  When the peak RH
	#  exceeds 1, then the threshold temperature has been reached.
	#  Prime slplume

	tls = -31.9
	slplume = [0.1]

	itamb = 1
	idelt = 1

	while (slplume[0] < 1) :
		tls = tls - 0.1
		tt = tls + t0

		# Ambient air density 
		rnair = (pamb / tt) / bk 

		# Liquid sat. H2O number density
		rnsatl = 1000. * np.exp(c1 + c2/tt + c3/(tt**2) + c4/(tt**3)) / bk / tt

		# Ice sat. H2O number density
		fexp = np.exp((bb - tls/bd) * tls / (tls + bc))
		rnsati = 1.e3 * ba * fexp / bk / (tls + t0) 

		# Ambient RHI
		rhiamb = rhamb * rnsatl/rnsati 

		# Ambient water vapor number density 
		# if the abmient RH > 1, then use RH = 1
		if (rhamb >= 0.9999) :
		  rnwamb = 0.9999 * rnsatl
		else :
		  rnwamb = rnsatl * rhamb  

		# Find the peak plume  saturation ratio by starting with a very large
		# deltaT (= Tplume-tls) and slowly decrementing deltaT until the peak
		# saturation is found.  i.e., start with conditions very near the
		# engine exit and move downstream.
		deltaT = 100.

		# Needs to be a list to access inside while loop
		##########################################
		############ plume = contrail ############
		##########################################
		slplume_prev = [0.]

		while (slplume[0] > slplume_prev[0]) :
		  slplume_prev[0] = slplume[0]

		  deltaT = deltaT / 1.3
		  tplume = tls + deltaT
		  tt = tplume + t0

		  # Liquid sat. H2O number density
		  rnsatl = 1000. * np.exp(c1 + c2/tt + c3/(tt**2) + c4/(tt**3)) / bk / tt

		  slplume[0] = (rnwamb/rnsatl + rnair * wexh * cp * rh2o * deltaT / 
		                                (rnsatl * delh * (1. - effic) * rd))

	# if tamb < Tls then contrail will form
	output = ""
	if tamb < tls :
		output = ("Pressure: " + str(pamb/1e3) + "mbar"+ " RHI: " + 
		          str(rhiamb * 100) + "% Tls: " + str(tls) + "C" +
		          " Tamb: " + str(tamb) + "C ---> PREDICTED"+ "\n")

		return output 
	else :
		return output 






