from generate_test_data import constant_density

import math

from electron import GetRingData
#from electron import CoulombForce

import numpy as np
import csv

# Simplest possible test case
# a point particle, and a point charge.
Coulomb_k = 9.0#*(10**7)
def GetRingData(src_file):
	csv = np.genfromtxt(src_file, delimiter = ',')
	angle = np.array(csv[1:,0])
	value = np.array(csv[1:,1])
	return angle, value

def CoulombForce(q1, q2, p1, p2):
	r = p2 - p1 #[b-a for a,b in zip(p1,p2)]
	#print("(%.2f, %.2f), (%.2f, %.2f), (%.2f, %.2f)\n" % (p2[0],p2[1], p1[0],p1[1], r[0],r[1]))
	r_squared = r.dot(r)*np.linalg.norm(r)#sum([a*a*abs(a) for a in r])
	#print r_squared
	return (r*Coulomb_k*q1*q2)/r_squared #[(Coulomb_k*q1*q2/r_squared)*vi for vi in r]

def run_simation(user_mass, user_charge, user_pos, user_vel, ring_radius, angle, value, n_steps):
	step = 0.001
	print user_pos
	p_new = user_pos
	myfile = open("output.csv","w")
	p_old = p_new
	for ui in range(n_steps):
		apply_force = CoulombForce(user_charge, value, p_new, np.array([0, 0]))
		#print ["%.2f " % el for el in p_new]
		# explicit eule
		#print apply_force

		#print("%.2f, %.2f\n" % (p_new[0], p_new[1]))

		'''if ui == 0:
			user_accel = apply_force/user_mass
			myfile.write("%.2f, %.2f, %.2f, %.2f\n" % (p_new[0], p_new[1],apply_force[0], apply_force[1]))
			p_new = p_new + 0.5*user_accel*step*step
			user_vel = user_vel + user_accel*step
		'''
		#else:
		user_accel = apply_force/user_mass
		myfile.write("%.2f, %.2f, %.2f, %.2f\n" % (p_new[0], p_new[1],apply_force[0]/20, apply_force[1]/20))
		p_new = p_new + user_vel*step + 0.5*user_accel*step*step
		user_vel = user_vel + 0.5*step*(user_accel+CoulombForce(user_charge, value, p_new, np.array([0, 0])))
		
		'''
			user_accel = apply_force/user_mass
			myfile.write("%.2f, %.2f, %.2f, %.2f\n" % (p_new[0], p_new[1],apply_force[0], apply_force[1]))
			temp = p_new
			p_new = 2*p_new - p_old + user_accel*step*step
			p_old = temp
		'''
#		print p_new, user_vel, user_accel


user_pos = np.array([0, 1.5])
user_mass = 1
user_charge = 1
ring_radius = 0

# Load data
angle, value = GetRingData('singulardist.csv')
print math.sqrt(Coulomb_k*user_charge*value/np.linalg.norm(user_pos)/user_mass)
user_vel = np.array([math.sqrt(Coulomb_k*user_charge*value/np.linalg.norm(user_pos)/user_mass), 0])

run_simation(user_mass, user_charge, user_pos, user_vel, ring_radius, angle, value, 100000)




#for a constant charge

#constant_density("5.0")

# test 1a repels 
# 1b cannot pass through?
# i  - approaching from orthogonal, will repel at predictable trajectory
'''
radius = 1.0
init_pos = [-10,0]
init_vel = [10,0]
...
'''
# ii - starting inside circle, there should be no electric field? b/c they are allowed to move. not fixed/rigid

# test 2 attracts (can pass through?)
# i - starting outside, finds final resting ...

# test 3 conserves over time (around the world)




'''
particle_dist = math.sqrt(sum([a*a for a in user_pos]))
q_ring = CalculateForce(user_charge, user_pos, ring_radius)
q_ring = [qr / Coulomb_k / user_charge for qr in q_ring]
q_ring = math.sqrt(sum([a*a for a in q_ring]))
# v_0 = 2*k*q_1*q_2/r_0/m
init_vel = [5.31,0.0]#2*Coulomb_k*user_charge*q_ring/particle_dist/particle_mass,0]

main(particle_mass, user_charge, user_pos, init_vel, ring_radius)
'''
#moving at a constant velocity, along a circular path of radius 10, 
#it should take exactly d = v*t => t = d/v => t = 2*pi*10/mag(init_vel)

