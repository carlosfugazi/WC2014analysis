def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc
    
def create_master_dict_of_city_coordinates():
	dict_ = {}
	# northeast
	dict_['Manaus']    = dict(lat=-3.1000, long=60.0167, abbrv='MNS')
	dict_['Fortaleza'] = dict(lat=-3.7737, long=38.5748, abbrv='FRT')
	dict_['Natal']  = dict(lat=-5.7833,long=35.2000, abbrv='NTL')    
	dict_['Recife'] = dict(lat=-8.0500,long=34.9000, abbrv='RCF')
	dict_['Brasilia']=dict(lat=-10.6500, long=52.9500, abbrv='BRA')
	dict_['Cuiaba'] =  dict(lat=-15.5958 , long=56.0969, abbrv='CBA')
	dict_['Salvador']=dict(lat=-12.9747 , long=38.4767, abbrv='SLV')
	dict_['Belo Horizonte']=dict(lat=-19.9167, long=43.9333, abbrv='BHZ')
	dict_['Rio de Janeiro']=dict(lat= -22.9083, long= 43.1964, abbrv='RdJ')
	dict_['Sao Paulo']=dict(lat=-23.5500, long= 46.6333, abbrv='SP')
	dict_['Curitiba']=dict(lat=-25.4167, long=49.2500, abbrv='CRB')
	dict_['Porto Alegre']=dict(lat=-30.0331, long= 51.2300, abbrv='PA')
	#print len(dict_.keys())
	return dict_
	
# what other info can I get based on lat, long? temp, humidity? 

def find_distance_between_two_cities(city1,city2,scale='mi'):
	
	dict_ = create_master_dict_of_city_coordinates()
	lat1 = dict_[city1]['lat']
	long1 = dict_[city1]['long']
	
	lat2 = dict_[city2]['lat']
	long2 = dict_[city2]['long']
	
	arc = distance_on_unit_sphere(lat1,long1,lat2,long2)
	#print arc, "R_e",
	#print arc*3960, "mi",
	#print arc*6373, 'km'
	if ( scale == 'mi'):
		return arc*3960
	elif( scale == 'km'):
		return arc*6373
	

#print find_distance_between_two_cities('Natal','Recife')
#print find_distance_between_two_cities('Recife','Fortaleza')
#print find_distance_between_two_cities('Natal','Fortaleza')

def print_distance_matrix():
	distances = []
	dict_ = create_master_dict_of_city_coordinates()
	#for key in dict_:
	#	print key
	cities = dict_.keys()
	print '{:16}'.format(''),
	for key in cities:
		print '{:<10}'.format(dict_[key]['abbrv']),	
	print ""
	for key in cities:
		print '{:16}'.format(key),
		for key_target in cities:
			if ( key != key_target):
				calc_dist = find_distance_between_two_cities(key,
					key_target)
				distances.append(calc_dist)
				print '{:<10.0f}'.format(calc_dist),
			else: print '{:<10}'.format(0)	,
		print ""
	print "max  distance (mi) : {:.0f}".format( max(distances) )
	print "min  distance (mi) : {:.0f}".format( min(distances) )
	print "mean distance (mi) : {:.0f}".format( mean(distances) )
	print "std  dev of ^ (mi) : {:.0f}".format( std(distances) )
	nice_histogram_plot(distances,div_miles=100.0)
	 
def nice_histogram_plot(tot_miles,div_miles=200.0,color='blue'):
	num_bins = int( max(tot_miles)-min(tot_miles) )/div_miles
	hist, bins = histogram( tot_miles, bins=num_bins)
	hist = [hist1 for hist1 in hist]
	#mu, sigma = 100, 15
	#x = mu + sigma * np.random.randn(10000)
	#hist, bins = np.histogram(x, bins=50)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	bar(center, hist, align='center', width=width, color=color)
	xlabel('Miles between match venues')
	ylabel('Frequency')

def create_dict_of_second_round_cities_to_final():
	fopen = open('knockoutdistances.csv','r')
	dict_ = {}
	for i,line in enumerate(fopen.readlines()):
		elements = (line.strip()).split(',')
		#print i+1,elements[0]
		dict_[elements[0]]=elements[1:]
	#print dict_
	return dict_
	
#test_second_round_cities
def analyze_second_round_distances(ploton=True):
	dict_all_distances = create_master_dict_of_city_coordinates()
	dict_second_round  = create_dict_of_second_round_cities_to_final()
	all_distances_dict = {}
	all_distances = []
	for key in dict_second_round:
		cities = dict_second_round[key]
		#print cities, len(cities)
		#for city in cities:
		#	if ( city in dict_all_distances):
		#		print True,
		total_distance = 0
		for i in [0,1,2]:
			calc_dist =  find_distance_between_two_cities(cities[i],
						cities[i+1])
			total_distance += calc_dist
		print total_distance
		all_distances.append(total_distance)
		all_distances_dict[key]=total_distance
	if ( ploton == True):
		figure(1); clf()
		nice_histogram_plot(all_distances,div_miles=50.0)
		show()
	return all_distances_dict
	
def plot_backround_image(image_file,axes1,alpha=0.25):
	import Image
	import numpy as np
	import matplotlib.mlab as mlab
	import matplotlib.pyplot as plt
	# league_logo_file = dict_league['Logo file']
	#if ( league_logo_file != None ):
	a = axes(axes1,frameon=False)
	im = Image.open(image_file)
	plt.imshow(im, origin='upper',alpha=alpha)
	xticks([])
	yticks([])
	ax = plt.gca()
	

#print_distance_matrix()
#create_dict_of_second_round_cities_to_final()
#analyze_second_round_distances()	