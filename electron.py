import sys

import ast
import csv

import math
import numpy as np


step = 0.01

Coulomb_k = 9.0#*(10**7)

class Particle:
	accel = np.array([0,0])

	def __init__(self, mass, charge, position, velocity):
		self.mass = mass
		self.charge =charge
		self.position = position
		self.velocity = velocity


class Ring:
	radius = 0
	charge_density = {} #angle, coulomb/cm

	def __init__(self, radius):
		self.radius = radius

	def ReadChargeDist(self, src_file):
		csv = np.genfromtxt(src_file, delimiter = ',')
		angles = np.array(csv[1:,0])
		values = np.array(csv[1:,1])
		self.charge_density = dict(zip(angles, values))
		print self.charge_density



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

def CalculateForce(user_charge, user_pos, my_ring):
	total_force = np.array([0,0])
	for a,v in my_ring.charge_density.iteritems():
		ring_pos = np.array([my_ring.radius*math.cos(math.radians(a)),my_ring.radius*math.sin(math.radians(a))])
		total_force = total_force+CoulombForce(user_charge,v, user_pos, ring_pos)
	return total_force

def simulate_step(my_particle, my_ring, step):
		my_particle.accel = CalculateForce(my_particle.charge, my_particle.position, my_ring)/my_particle.mass
		p_new = my_particle.position + my_particle.velocity*step + 0.5*my_particle.accel*step*step
		future_accel = CalculateForce(my_particle.charge, p_new, my_ring)/my_particle.mass
		my_particle.velocity = my_particle.velocity + 0.5*step*(my_particle.accel+ future_accel)
		return p_new, my_particle.velocity

def run_simution(my_particle, my_ring, n_steps):
	print my_particle.position
	myfile = open("output.csv","w")
	for ui in range(n_steps):
		new_pos, new_vel = simulate_step(my_particle, my_ring, step)
		myfile.write("%d, %.2f, %.2f\n" % (ui, my_particle.position[0], my_particle.position[1]))
	return my_particle.position, my_particle.velocity

'''
def main(user_mass, user_charge, user_pos, user_vel, ring_radius, angles, values):
	#user_charge = eval(raw_input("input charge: "))
	#user_pos = [px[0],py[0]]#eval(raw_input("input '[x,y]': "))
	#user_mass = 1.0
	#ring_radius = 5.0
	#user_vel = [vx[0],vy[0]]#[0.0,0.0]
	print user_vel
	#SaveRingData(ring_radius)

	step = 0.0005
	# for some number of steps
	p_new = user_pos
	myfile = open("output.csv","w")
	for ui in range(200):
		# determine the force at that moment
		apply_force = CalculateForce(user_charge, p_new, ring_radius, angles, values)

		# calcuate the future position
		user_accel = apply_force#/user_mass
		print ["%.2f " % el for el in p_new]
		myfile.write("%.2f, %.2f, %.2f, %.2f\n" % (p_new[0], p_new[1],apply_force[0]/20, apply_force[1]/20))

		p_new = [po + v+step + 0.5*a*step*step for po, v, a in zip(p_new, user_vel, user_accel)]
		user_vel = [v + a*step for v, a in zip(user_vel, user_accel)]
		# print ["%.2f " % el for el in p_new]
		#myfile.write("%.2f, %.2f, %.2f, %.2f\n" % (p_new[0], p_new[1],apply_force[0]/20, apply_force[1]/20))
		#for ui, el in enumerate(p_new):
		#	if ui < len(p_new)-1:
		#		myfile.write("%.2f, " % el)
		#	else:
		#		myfile.write("%.2f, %.2f, %.2f\n" % (el, apply_force[0], apply_force[1]))
	#		print type(user_charge_pos)

'''

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
	mass = eval(sys.argv[1])
	charge = eval(sys.argv[2])
	px = eval(sys.argv[3])
	py = eval(sys.argv[4])
	vx = eval(sys.argv[5])
	vy = eval(sys.argv[6])
	rad = eval(sys.argv[7])

	print mass, charge, px, py, vx, vy, rad
	main(mass, charge, [px, py], [vx, vy], rad)
	'''
	 plot 'C:/ringdata.csv' using 1:2:3 palette, 'C:/output.csv' using 1:2, 'C:/output.csv' using 1:2 wit
h lines, 'C:/output.csv' using 1:2:3:4 with vectors
	'''