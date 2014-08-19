import random
#m=7
#p=11
#r=3
#z=100 + x
M0 = 7
Prime = 101
def rushp(x,replic):
	l = []
	for r in xrange(replic):
		random.seed(x)
		z = random.randint(0,100 + M0)
		v = x + z +  r * Prime
		l.append(v % M0)
	return l
def summary():
	x = {0:0,1:0,2:0,3:0,4:0,5:0,6:0}
	for i in xrange(100000):
		for j in rushp(i,2):
			x[j] = x[j] + 1
	print x

summary()
