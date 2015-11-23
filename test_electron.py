from generate_test_data import constant_density
import math
import electron
import Estimator
import numpy as np
import csv

# Simplest possible test case
# a point particle, and a point charge.
'''
Coulomb_k = 9.0#*(10**9)

# One Element tests

# moving at a constant velocity, along a circular path of radius 10, 
# it should take exactly d = v*t => t = d/v => t = 2*pi*radius/mag(init_vel)

print "Test 1: complete the circle"
user_pos = np.array([0, 1.5])
user_mass = 1
user_charge = 1
ring_radius = 0

Estimator.dt = 0.001

my_ring = electron.Ring(ring_radius)
my_ring.ReadChargeDist('singulardist.csv')

Estimator.my_ring = my_ring

user_vel = np.array([math.sqrt(Coulomb_k*user_charge*my_ring.charge_density[0]/np.linalg.norm(user_pos)/user_mass), 0])

time_limit = 2.0*math.pi*np.linalg.norm(user_pos)/np.linalg.norm(user_vel)/Estimator.dt

user_accel = electron.CalculateForce(user_charge, user_pos, my_ring)
my_particle = electron.Particle(user_mass, user_charge, user_pos, user_vel, user_accel)

my_state = electron.State(my_particle, 0)
my_system = electron.System(my_state)

final_pos, final_vel = electron.run_simulation(my_system, int(time_limit))

#final_pos, final_vel = run_simution(user_mass, user_charge, user_pos, user_vel, ring_radius, angle, value, int(time_limit))
# expect. final position to equal first position.
print user_pos, final_pos, np.linalg.norm(final_pos - user_pos)

'''
'''

print "Test 2: Conserves Energy"
user_pos = np.array([0, 10])
user_mass = 1.0
user_charge = 1.0
ring_radius = 0

# Load data
#angle, value = GetRingData('singulardist.csv')
user_vel = np.array([0, 0])

my_ring = electron.Ring(ring_radius)
my_ring.ReadChargeDist('singulardist.csv')

Estimator.my_ring = my_ring

user_vel = np.array([0, 0])
user_accel = electron.CalculateForce(user_charge, user_pos, my_ring)
print user_accel
my_particle = electron.Particle(user_mass, user_charge, user_pos, user_vel, user_accel)

my_state = electron.State(my_particle, 0)
my_system = electron.System(my_state)

final_pos, final_vel = electron.run_simulation(my_system, 500)
print final_vel
#final_pos, final_vel = run_simution(user_mass, user_charge, user_pos, user_vel, ring_radius, angle, value, 10)
print Coulomb_k*(my_ring.charge_density[0])*user_charge*(1.0/np.linalg.norm(user_pos) - 1.0/np.linalg.norm(final_pos)) - 0.5*user_mass*np.linalg.norm(final_vel)**2
'''

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
'''


import unittest
import numpy as np
import generate_test_data as gen_data

Coulomb_k = 9.0#*(10**9)

class ElectronTestCase(unittest.TestCase):
	
	# One Element tests

	# moving at a constant velocity, along a circular path of radius 10, 
	# it should take exactly d = v*t => t = d/v => t = 2*pi*radius/mag(init_vel)
	def test_completes_the_circle(self):
		gen_data.singular('5.0')

		print "Test 1: complete the circle"
		acceptable_rmse = 0.01

		user_pos = np.array([0, 1.5])
		user_mass = 1
		user_charge = 1
		ring_radius = 0

		my_ring = electron.Ring(ring_radius)
		my_ring.ReadChargeDist('singulardist.csv')

		Estimator.dt = 0.001
		Estimator.my_ring = my_ring

		user_vel = np.array([math.sqrt(Coulomb_k*user_charge*my_ring.charge_density[0]/np.linalg.norm(user_pos)/user_mass), 0])

		time_limit = 2.0*math.pi*np.linalg.norm(user_pos)/np.linalg.norm(user_vel)/Estimator.dt

		user_accel = electron.CalculateForce(user_charge, user_pos, my_ring)
		my_particle = electron.Particle(user_mass, user_charge, user_pos, user_vel, user_accel)

		my_state = electron.State(my_particle, 0)
		my_system = electron.System(my_state)

		final_pos, final_vel = electron.run_simulation(my_system, int(time_limit))

		# Expect final position to equal first position.
		print np.linalg.norm(final_pos - user_pos)

		self.assertTrue(np.linalg.norm(final_pos - user_pos) < acceptable_rmse)

	# From far away everything looks like a point charge. Drifting towards the
	# charge any loss in electric potential should be found in kinetic energy
	def test_same_from_afar(self):
		print "Test 2: Conserves Energy"
		acceptable_error = 0.01

		user_pos = np.array([0, 10])
		user_mass = 1.0
		user_charge = 1.0
		ring_radius = 0

		user_vel = np.array([0, 0])

		my_ring = electron.Ring(ring_radius)
		my_ring.ReadChargeDist('singulardist.csv')

		Estimator.my_ring = my_ring

		user_vel = np.array([0, 0])
		user_accel = electron.CalculateForce(user_charge, user_pos, my_ring)
		
		my_particle = electron.Particle(user_mass, user_charge, user_pos, user_vel, user_accel)

		my_state = electron.State(my_particle, 0)
		my_system = electron.System(my_state)

		final_pos, final_vel = electron.run_simulation(my_system, 100)
		print Coulomb_k*(my_ring.charge_density[0])*user_charge*(1.0/np.linalg.norm(user_pos) - 1.0/np.linalg.norm(final_pos)) - 0.5*user_mass*np.linalg.norm(final_vel)**2
		#final_pos, final_vel = run_simution(user_mass, user_charge, user_pos, user_vel, ring_radius, angle, value, 10)
		self.assertTrue(math.fabs(Coulomb_k*(my_ring.charge_density[0])*user_charge*(1.0/np.linalg.norm(user_pos) - 1.0/np.linalg.norm(final_pos)) - 0.5*user_mass*np.linalg.norm(final_vel)**2) < 0.1)

	# In the presence of a few (in this case 2) charges, a point with no net force should exist
	def test_for_minimum(self):
		print "Test 3: find the well"
		acceptable_error = 0.001
		user_mass = 1.0
		user_charge = -1.0
		ring_radius = 5.0
		user_pos = np.array([0, ring_radius*(-1.0+ 2.0/(1.0+math.sqrt(2.0)))])

		my_ring = electron.Ring(ring_radius)
		my_ring.ReadChargeDist('bipolardist.csv')

		user_vel = np.array([0, 0])
		user_accel = electron.CalculateForce(user_charge, user_pos, my_ring)
		my_particle = electron.Particle(user_mass, user_charge, user_pos, user_vel, user_accel)

		my_state = electron.State(my_particle, 0)
		my_system = electron.System(my_state)

		final_pos, final_vel = electron.run_simulation(my_system, 1000)

		print np.linalg.norm(final_pos - user_pos), np.linalg.norm(final_vel- user_vel)
		# same position
		self.assertTrue(np.linalg.norm(final_pos - user_pos) < acceptable_error)
		# not moving
		self.assertTrue(np.linalg.norm(final_vel- user_vel) < acceptable_error)

if __name__ == '__main__':
	unittest.main()
