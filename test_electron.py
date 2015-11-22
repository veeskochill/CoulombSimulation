from generate_test_data import constant_density

import math

from electron import GetRingData
#from electron import CoulombForce

import numpy as np
import csv

# Simplest possible test case
# a point particle, and a point charge.
step = 0.01

Coulomb_k = 9.0#*(10**7)

def SaveRingData(filename, ring_radius):
	csv = np.genfromtxt(filename, delimiter = ',')
	angle = csv[1:,0]
	value = csv[1:,1]
	myfile = open("ringdata.csv","w")
	for a,v in zip(angle, value):
		#print math.cos(math.radians(a)), math.sin(math.radians(a)), v
		myfile.write("%.2f, %.2f, %.2f\n" % (ring_radius*math.cos(math.radians(a)), ring_radius*math.sin(math.radians(a)), v))
	myfile.close()

def GetRingData(src_file):
	csv = np.genfromtxt(src_file, delimiter = ',')
	angle = np.array(csv[1:,0])
	value = np.array(csv[1:,1])
	return angle, value

def CoulombForce(q1, q2, p1, p2):
	r = p2 - p1
	r_squared = r.dot(r)*np.linalg.norm(r)
	return (r*Coulomb_k*q1*q2)/r_squared

def CalculateForce(user_charge, value, user_pos, angle, ring_radius):
	total_force = np.array([0,0])
	for a,v in zip(angle, value):
		ring_pos = np.array([ring_radius*math.cos(math.radians(a)),ring_radius*math.sin(math.radians(a))])
		total_force = total_force+CoulombForce(user_charge,v, user_pos, ring_pos)
	return total_force

def simulate_step(user_mass, user_charge, user_pos, user_vel, ring_radius, angle, value, step):
		user_accel = CalculateForce(user_charge, value, user_pos, angle, ring_radius)/user_mass
		p_new = user_pos + user_vel*step + 0.5*user_accel*step*step
		future_accel = CalculateForce(user_charge, value, p_new, angle, ring_radius)/user_mass
		user_vel = user_vel + 0.5*step*(user_accel+ future_accel)
		return p_new, user_vel

def run_simution(user_mass, user_charge, user_pos, user_vel, ring_radius, angle, value, n_steps):
	print user_pos
	new_pos = user_pos
	new_vel = user_vel
	myfile = open("output.csv","w")
	for ui in range(n_steps):
		new_pos, new_vel = simulate_step(user_mass, user_charge, new_pos, new_vel, ring_radius, angle, value, step)
		myfile.write("%d, %.2f, %.2f\n" % (ui, new_pos[0], new_pos[1]))
	return new_pos, new_vel


'''
# One Element tests
{
	print "Test 1: complete the circle"
	user_pos = np.array([0, 1.5])
	user_mass = 1
	user_charge = 1
	ring_radius = 0

	# Load data
	angle, value = GetRingData('singulardist.csv')
	print math.sqrt(Coulomb_k*user_charge*value/np.linalg.norm(user_pos)/user_mass)
	user_vel = np.array([math.sqrt(Coulomb_k*user_charge*value/np.linalg.norm(user_pos)/user_mass), 0])

	time_limit = 2.0*math.pi*np.linalg.norm(user_pos)/np.linalg.norm(user_vel)/step
	print time_limit

	final_pos, final_vel = run_simution(user_mass, user_charge, user_pos, user_vel, ring_radius, angle, value, int(time_limit))
	# expect. final position to equal first position.
	print user_pos, final_pos, np.linalg.norm(final_pos - user_pos)
}
'''

'''
{
	print "Test 2: Conserves Energy"
	user_pos = np.array([0, 10])
	user_mass = 1
	user_charge = 1
	ring_radius = 0

	# Load data
	angle, value = GetRingData('singulardist.csv')
	user_vel = np.array([0, 0])


	final_pos, final_vel = run_simution(user_mass, user_charge, user_pos, user_vel, ring_radius, angle, value, 10)
	print Coulomb_k*value*user_charge*(1.0/np.linalg.norm(user_pos) - 1.0/np.linalg.norm(final_pos)) - 0.5*user_mass*np.linalg.norm(final_vel)**2
}
'''

# Two element tests
{
	print "Test 3: find the well"
	user_mass = 1
	user_charge = -1
	ring_radius = 5
	user_pos = np.array([0, ring_radius*(-1.0+ 2.0/(1.0+math.sqrt(2.0)))])
	print user_pos
	angle, value = GetRingData('bipolardist.csv')
	SaveRingData('bipolardist.csv', ring_radius)

	user_vel = np.array([0, 0])

	final_pos, final_vel = run_simution(user_mass, user_charge, user_pos, user_vel, ring_radius, angle, value, 200)

	print np.linalg.norm(final_pos - user_pos), np.linalg.norm(final_vel- user_vel)
}

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

