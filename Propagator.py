import electron

# Responsible for implementing numerical methods
dt = 0.01
method = 'leapfrog'

# Numerical methods should be separated from the system itself. 
def leapfrog(my_particle, my_ring):
	x_n = my_particle.position
	v_n = my_particle.velocity
	a_n = my_particle.accel

	x_n1 = x_n + dt*v_n + 0.5*a_n*dt*dt # calculate
	a_n1 = electron.CalculateForce(my_particle.charge, x_n1, my_ring)/my_particle.mass # update
	v_n1 = v_n +0.5*dt*(a_n1 + a_n) # calculate
	updated_particle = electron.Particle(my_particle.mass, my_particle.charge, my_particle.position, my_particle.velocity, a_n1)
	return updated_particle, dt 

def step_forward(my_particle, my_ring):
	if method == 'leapfrog':
		return leapfrog(my_particle, my_ring)