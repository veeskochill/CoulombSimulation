from generate_test_data import constant_density

import math

import electron

import numpy as np
import csv

# Simplest possible test case
# a point particle, and a point charge.
step = 0.01

Coulomb_k = 9.0#*(10**7)

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
print "Test 3: find the well"
user_mass = 1
user_charge = -1
ring_radius = 5
user_pos = np.array([0, ring_radius*(-1.0+ 2.0/(1.0+math.sqrt(2.0)))])
print user_pos
#angle, value = electron.GetRingData('bipolardist.csv')
#electron.SaveRingData('bipolardist.csv', ring_radius)

my_ring = electron.Ring(ring_radius)
my_ring.ReadChargeDist('bipolardist.csv')

user_vel = np.array([0, 0])
user_accel = electron.CalculateForce(user_charge, user_pos, my_ring)
my_particle = electron.Particle(user_mass, user_charge, user_pos, user_vel, user_accel)

my_state = electron.State(my_particle, 0)
my_system = electron.System(my_state)

final_pos, final_vel = electron.run_simulation(my_system, 200)

print np.linalg.norm(final_pos - user_pos), np.linalg.norm(final_vel- user_vel)


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

