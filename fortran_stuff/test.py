
g = [0]

while (g[0] < 10) :

	while (g[0] < 5) :
		print 'inside g: ' + str(g[0])
		g[0] = g[0] + 1 

	g[0] = g[0] + 1

print "g: " + str(g[0])
