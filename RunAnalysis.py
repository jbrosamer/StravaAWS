import math


def riegelFormula(newDist, oldDist, oldTime):
	return oldTime*math.pow(newDist/oldDist, 1.06)

def cameronFormula(newDist, oldDist, oldTime):
	a=13.49681-(0.000030363*oldDist)+(835.7114/math.pow(oldDist, 0.7905))
	b=13.49681-(0.000030363*newDist)+(835.7114/math.pow(newDist, 0.7905))
	return (oldTime/oldDist)*(a/b)*newDist