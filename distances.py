import os, sys
execfile('calculate_distance.py')

def get_master_first_round_dict():
	dict_= {}
	fopen = open('distances2.csv','r')
	lines = fopen.readlines()
	keys = (lines[0].strip()).split(',')[1:]
	print keys
	for line in lines[1:]:
		#print line.strip()
		elements = (line.strip()).split(',')
		sub_dict = {}
	
		for key,element in zip(keys,elements[1:]):
			try: 
				sub_dict[key] = eval(element)
			except:
				sub_dict[key] = element
		dict_[elements[0]]=sub_dict
		#break
	return dict_
	#print dict_

def get_master_first_round_dict_2():
	dict_= {}
	fopen = open('distances3.csv','r')
	lines = fopen.readlines()
	keys = (lines[0].strip()).split(',')[0:]
	#print keys
	#stop_here
	for line in lines[1:]:
		#print line.strip()
		elements = (line.strip()).split(',')
		sub_dict = {}
	
		for key,element in zip(keys,elements[0:]):
			try:
				sub_dict[key] = eval(element)
			except:
				sub_dict[key] = element
		dict_[elements[1]]=sub_dict
		#break
	#print dict_
	#stop_here
	return dict_

dict_ = get_master_first_round_dict_2()

#dict_ = get_master_first_round_dict()
#
# analyze group
#
letters = ['A','B','C','D','E','F','G','H']
tmgs, rmgs = [], []
dict_teams_by_code  = {}
for letter in letters:
	tot_miles_for_group = []
	tot_miles_for_team  = []
	
	for i in range(1,4+1,1):
		group_member = '{}{}'.format(letter,i)
		
		#tot_miles_for_team 
		print '{:2} {:4}'.format(group_member,
			dict_[group_member]['XTOT']),
		tot_miles_for_group.append( dict_[group_member]['XTOT'] )
		dict_teams_by_code[group_member] = dict_[group_member]['XTOT']
		
 	print " Total for group {} : ".format(letter), \
 		sum(tot_miles_for_group),
	print " Range for group {} : ".format(letter),\
		max(tot_miles_for_group)-min(tot_miles_for_group) 
		
	tmg, rmg = sum(tot_miles_for_group), max(tot_miles_for_group)-min(tot_miles_for_group) 
	tmgs.append(tmg); rmgs.append(rmg)
	
N = 32
figure(1);
clf()
#plot( range(1,32+1,1), [ dict_[key]['XTOT'] for key in dict_ ])
tot_miles = array( [ dict_[key]['XTOT'] for key in dict_ ] )
num_bins = int( max(tot_miles)-min(tot_miles) )/200.0
hist, bins = histogram( tot_miles, bins=num_bins)

#mu, sigma = 100, 15
#x = mu + sigma * np.random.randn(10000)
#hist, bins = np.histogram(x, bins=50)
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
bar(center, hist, align='center', width=width)
xlabel('Miles traveled between group game cities')
ylabel('Frequency')
#tight_layout()
show()

close(1)
figure(2);
clf()
xlabel('Miles traveled between group game cities')
ylabel('Range in total miles traveled within group')

offsetsy = [0, 0, 100, 0, 0, -100, 0, 0 ]
colors = ['r','r','b','b','g','g','k','k']
for i in range(len(rmgs)):
	text(tmgs[i]+200,rmgs[i]+offsetsy[i],letters[i],fontsize=20.)	
	plot(tmgs[i],rmgs[i],'o',markeredgecolor=colors[i],markersize=10.0,mfc='none',
		markeredgewidth=3.0)

for i in range(4):
	plot(tmgs[2*i:2*i+1+1],rmgs[i*2:2*i+1+1],'--',
		color=colors[2*i],alpha=0.6,linewidth=2.0)

figure(3);
clf()
plane_velocity = 450. #mph

ylabel('Range in airplane time')
xlabel('Total airplane time assuming {} mph'.format(plane_velocity))

offsetsy = [0, 0, 1/4., 0, 0, -1/4., 0, 0 ]
colors = ['r','r','b','b','g','g','k','k']
for i in range(len(rmgs)):
	text(tmgs[i]/plane_velocity+0.3,rmgs[i]/plane_velocity+offsetsy[i],letters[i],fontsize=20.)	
	plot(tmgs[i]/plane_velocity,rmgs[i]/plane_velocity,'o',markeredgecolor=colors[i],markersize=10.0,mfc='none',
		markeredgewidth=3.0)

for i in range(4):
	plot(array(tmgs[2*i:2*i+1+1])/plane_velocity,array(
		rmgs[i*2:2*i+1+1])/plane_velocity,'--',
		color=colors[2*i],alpha=0.6,linewidth=2.0)

figure(4);
# analysis of all possibilities to get to final
# group A
print dict_teams_by_code
all_possible_paths = []
dict_2 =analyze_second_round_distances(ploton=False)
print len(dict_teams_by_code.keys())
keys = []
for i,key in enumerate(dict_teams_by_code):
	#print dict_teams_by_code[key],
	#print i+1," group ",key[0], "team ", key[1]
	case1 = dict_2['1{}'.format(key[0])]
	case2 = dict_2['2{}'.format(key[0])]
	all_possible_paths.append( dict_teams_by_code[key] + case1)
	keys.append( [key,'1st'] )
	all_possible_paths.append( dict_teams_by_code[key] + case2)
	keys.append( [key,'2nd'] )
#
# final plot	
#

	

for func1 in [max,min]:
	#print func1 
	index1 = all_possible_paths.index(func1(all_possible_paths))
	key = keys[index1][0]
	print "{} travel distance for team {} {} {} is {}".format(func1,
		key,
		dict_[ key ]['Team'],
		keys[index1][1],
		func1(all_possible_paths) )

selected_keys = [ ['A1','1st'], ['A1','2nd'],['B1','1st'],['B1','2nd']
	,['G1','1st'],['G1','2nd'],['F1','1st'],['F1','2nd'] ]
#brazil,spain,germany,argentina
selected_paths = []
for key in selected_keys:
	index1 = keys.index(key)
	#print index1	
	print "{} travel distance for team {} {} {} is {}".format(key,
		key[0],
		dict_[ key[0] ]['Team'],
		keys[index1][1],
		all_possible_paths[index1] )
	selected_paths.append(all_possible_paths[index1])
close(2);close(3);close(4)
figure(1); clf()	
#print "min travel distance for team {} {} is {}".format( 
#	keys[ all_possible_paths.index(min(all_possible_paths))][0],
#	keys[ all_possible_paths.index(min(all_possible_paths))][1], min(all_possible_paths) )
kwargs=dict()
plot_backround_image('images/1000px-WC-2014-Brasil.png',[0.05, 0.1, .90, .80],alpha=0.41)
flag_alpha=0.75
plot_backround_image('images/1000px-Flag_of_Brazil.png',[0.638, 0.65, .10, .10],alpha=flag_alpha)
plot_backround_image('images/1000px-Flag_of_Spain.png',[0.252, 0.65, .10, .10],alpha=flag_alpha)
plot_backround_image('images/1000px-Flag_of_Germany.png',[0.115, 0.325, .10, .10],alpha=flag_alpha)
plot_backround_image('images/1000px-Flag_of_Argentina.png',[0.31, 0.80, .10, .10],alpha=flag_alpha)

plot_backround_image('images/Twitter_bird_logo_2012.png',[0.125,0.90,0.10,0.10],alpha=0.75)
axes([0.1,0.125,0.8,0.79],frameon=False)
nice_histogram_plot(all_possible_paths,div_miles=100.0,color=(0,172/(255.),237/(255.)))

print("mean(all_possible_paths)", mean(all_possible_paths))
#axvline(x=selected_paths[0],color='green',linestyle='dashed',linewidth=3.0)
#axvline(x=selected_paths[2],color='red',linestyle='dashed',linewidth=3.0)
#axvline(x=selected_paths[4],color='black',linestyle='dashed',linewidth=3.0)
#axvline(x=selected_paths[6],color='cyan',linestyle='dashed',linewidth=3.0)
vline_alpha=0.85
vlines(selected_paths[0],2,4.85+1.2,color='green',linestyle='dashed',linewidth=2.0,alpha=vline_alpha)
vlines(selected_paths[2],4,4.80+1.3,color='red',linestyle='dashed',linewidth=2.0,alpha=vline_alpha)
vlines(selected_paths[4],1,1.9+1.0,color='black',linestyle='dashed',linewidth=2.0,alpha=vline_alpha)
vlines(selected_paths[6],3.0,6.16+1.4,color=(0,132/(255.),180/(255.)),linestyle='dashed',linewidth=2.0,alpha=vline_alpha)
ylim([0,8])

title('@arsfutbolistica',fontsize=40,color=(0,172/(255.),237/(255.)),style='italic',
	alpha=0.99)
# grid(True)
xlabel('\nTotal miles travelled between match venues to reach Final',fontsize=18,style='italic')
ylabel('Frequency\n',fontsize=18,style='italic')

savefig('figure_test.png')
savefig('distribution_of_totaltravel_to_final_dpi.pdf',dpi=300)