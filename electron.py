'''
 keep it simple.
 don't worry about mag fields, or step-size error
'''

import sys

import ast
import csv

import math
import numpy as np


# return the CoulombForce between two charged particles\
def CoulombForce(q1, q2, p1, p2):
	Coulomb_k = 9.0
	r = [b-a for a,b in zip(p1,p2)]
	#print("(%.2f, %.2f), (%.2f, %.2f), (%.2f, %.2f)\n" % (p2[0],p2[1], p1[0],p1[1], r[0],r[1]))
	r_squared = sum([a*a*abs(a) for a in r])
	#return r
	return [(Coulomb_k*q1*q2/r_squared)*vi for vi in r]

def SaveRingData(ring_radius):
	csv = np.genfromtxt('chargedist.csv', delimiter = ',')
	angle = csv[1:,0]
	value = csv[1:,1]
	myfile = open("ringdata.csv","w")
	for a,v in zip(angle, value):
		print math.cos(math.radians(a)), math.sin(math.radians(a)), v
		myfile.write("%.2f, %.2f, %.2f\n" % (ring_radius*math.cos(math.radians(a)), ring_radius*math.sin(math.radians(a)), v))
	myfile.close()


def GetRingData(src_file):
	csv = np.genfromtxt(src_file, delimiter = ',')
	angle = csv[1:,0]
	value = csv[1:,1]
	return angle, value

def CalculateForce(user_charge, user_pos, ring_radius):
	angle, value = GetRingData('chargedist.csv')
	total_force =[0,0]
	for a,v in zip(angle, value):
		ring_pos = [ring_radius*math.cos(math.radians(a)),ring_radius*math.sin(math.radians(a))]
		total_force = [a+b for a,b in zip(total_force,CoulombForce(user_charge,v, user_pos, ring_pos))]
	return total_force

def main():
	user_charge = eval(raw_input("input charge: "))
	user_pos = eval(raw_input("input '[x,y]': "))
	user_mass = 1.0
	ring_radius = 5.0
	user_vel = [0.0,0.0]

	SaveRingData(ring_radius)

	step = 0.0005
	# for some number of steps
	p_new = user_pos
	myfile = open("output.csv","w")
	for ui in range(200):
		# determine the force at that moment
		apply_force = CalculateForce(user_charge, p_new, ring_radius)

		# calcuate the future position
		user_accel = apply_force#/user_mass
		p_new = [po + v+step + 0.5*a*step*step for po, v, a in zip(p_new, user_vel, user_accel)]
		user_vel = [v + a*step for v, a in zip(user_vel, user_accel)]
		print ["%.2f " % el for el in p_new]
		myfile.write("%.2f, %.2f, %.2f, %.2f\n" % (p_new[0], p_new[1],apply_force[0]/20, apply_force[1]/20))
		'''for ui, el in enumerate(p_new):
			if ui < len(p_new)-1:
				myfile.write("%.2f, " % el)
			else:
				myfile.write("%.2f, %.2f, %.2f\n" % (el, apply_force[0], apply_force[1]))
		'''
#		print type(user_charge_pos)



if __name__ == "__main__":
	num_arg = len(sys.argv)
	str(sys.argv)
	#sys.argv[0] is filename
	'''
	mass
	charge
	init position
	init velocity
	radius of ring
	'''
	main()