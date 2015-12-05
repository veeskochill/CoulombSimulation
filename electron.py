import sys
import ast
import csv
import math
import numpy as np
import Estimator

Coulomb_k = 9.0#*(10**9)

def CoulombForce(q1, q2, p1, p2):
	r = p2 - p1
	r_squared = r.dot(r)*np.linalg.norm(r)
	return (r*Coulomb_k*q1*q2)/r_squared

# This does not currently numerically integrate over the length of the arc
# It simply treats the charge density as the charge value at that point
# Currently sums the force for a point charge at each angle given
def CalculateForce(user_charge, user_pos, my_ring):
	total_force = np.array([0,0])
	for a,v in my_ring.charge_density.iteritems():
		ring_pos = np.array([my_ring.radius*math.cos(math.radians(a)),my_ring.radius*math.sin(math.radians(a))])
		total_force = total_force+CoulombForce(user_charge,v, user_pos, ring_pos)
	return total_force

# Responsible for moving the system the current state to the next state
class System:
	# it stores all previous states (This could be useful to keep for some predictor methods)
	states = []

	# a system must have an inital state, but has a default step size
	def __init__(self, state):
		self.states = [state]
	
	def step_forward(self):
		next_state = self.states[len(self.states)-1].step_forward()
		self.states.append(next_state)
		return next_state


# Responsible for maintaining a history of the particle-ring system
class State:

	def __init__(self, particle, time):
		self.time = time
		self.particle = particle

	def step_forward(self):
		updated_particle, dt = self.particle.step_forward()
		updated_state = State(updated_particle, self.time + dt)
		return updated_state


# Responsible for storage of particle properties
class Particle:

	def __init__(self, mass, charge, position, velocity, accel):
		self.mass = mass
		self.charge = charge
		self.position = position
		self.velocity = velocity
		self.accel = accel

	def step_forward(self):
		return Estimator.step_forward(self)


# Responsible for storage of ring properties
class Ring:

	radius = 0
	charge_density = {} # angle: coulomb/cm

	def __init__(self, radius):
		self.radius = radius

	def ReadChargeDist(self, src_file):
		csv = np.genfromtxt(src_file, delimiter = ',')
		angles = np.array(csv[1:,0])
		values = np.array(csv[1:,1])
		self.charge_density = dict(zip(angles, values))

def run_simulation(my_system, n_steps, output_file):

	myfile = open(output_file,"w")
	for ui in range(n_steps):
		new_state = my_system.step_forward()
		myfile.write("%.2f, %.2f, %.2f\n" % (new_state.time, new_state.particle.position[0], new_state.particle.position[1]))
	return new_state.particle.position, new_state.particle.velocity


if __name__ == "__main__":
	num_arg = len(sys.argv)
	str(sys.argv)

	mass = eval(sys.argv[1])
	charge = eval(sys.argv[2])
	px = eval(sys.argv[3])
	py = eval(sys.argv[4])
	vx = eval(sys.argv[5])
	vy = eval(sys.argv[6])
	rad = eval(sys.argv[7])

	main(mass, charge, [px, py], [vx, vy], rad)
