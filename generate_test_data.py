import sys, getopt

def singular(charge):
	fp = open("singulardist.csv", "w") 
	fp.write("Angle (degrees), linear charge density(microcoluomb/cm)\n")
	fp.write("%d, %.2f\n" % (0, eval(charge)))


def constant_density(charge):
	fp = open("constantdist.csv", "w") 
	fp.write("Angle (degrees), linear charge density(microcoluomb/cm)\n")
	for ui in range(360):
		fp.write("%d, %.2f\n" % (ui, eval(charge)))

def polarized_density(charge):
	fp = open("bipolardist.csv", "w") 
	fp.write("Angle (degrees), linear charge density(microcoluomb/cm)\n")
	#for ui in range(180):
	fp.write("%d, %.2f\n" % (90, eval(charge)))
	#for ui in range(180):
	fp.write("%d, %.2f\n" % (270, eval(charge)/2))

# This is intended to provide command line options for generating test data
def main(argv):
	try:
		opts, args = getopt.getopt(argv, "p::",["const=","polar=","sing="])
	except getopt.GetoptError:
		print 'generate.py -c <constant_charge_value> -p <polarized_charge_value>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-c","const="):
			constant_density(arg)
		elif opt in ("-p","polar="):
			polarized_density(arg)
		elif opt in("-s","sing="):
			singular(arg)

if __name__ == "__main__":
	main(sys.argv[1:])

