# Numerical methods should be separated from the system itself. 
# They need to act on the system from outside.
# As a python module I can update the timestep, dt
# and even the method used between simulation steps.

import electron

# Responsible for implementing numerical methods
dt = 0.01
method = 'leapfrog'
my_ring = None

def leapfrog(my_particle):
	x_n = my_particle.position
	v_n = my_particle.velocity
	a_n = my_particle.accel


	x_n1 = x_n + dt*v_n + 0.5*a_n*dt*dt # calculate
	a_n1 = electron.CalculateForce(my_particle.charge, x_n1, my_ring)/my_particle.mass # update
	v_n1 = v_n +0.5*dt*(a_n1 + a_n) # calculate

	updated_particle = electron.Particle(my_particle.mass, my_particle.charge, x_n1, v_n1, a_n1)
	return updated_particle, dt 

def step_forward(my_particle):
	if method == 'leapfrog':
		return leapfrog(my_particle)