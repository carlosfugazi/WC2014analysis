#
# analyze FIFA rankings in 2010
#
from difflib import get_close_matches

def load_dict_ranking_from_file(filename1):
	# filename1 = 'top_60_FIFA_ranking_May_2010.txt'
	fopen = open(filename1,'r')
	lines = fopen.readlines()
	dict_ = {}
	#
	#	 header
	#
	dict_['date']         = lines[0].strip()
	#dict_['num_of_teams'] = len(lines[2:])
	dict_teams = {}
	dict_rankings = {}
	for line1 in lines[2:]:
		elements = line1.split()
		num_elements = len(elements)
		num_of_team_str_elements = num_elements-4
		team_str     = ('{} '*(num_elements-4)).format(*elements[1:1+(num_elements-4)])
		team_str     = team_str.strip()
		dict_teams[team_str]=dict(rank=eval(elements[0]),points=eval(elements[1+num_of_team_str_elements]),
			change_in_position=eval(elements[1+num_of_team_str_elements+1]) )
		dict_rankings[elements[0]]=dict(team=team_str,points=eval(elements[1+num_of_team_str_elements]),
			change_in_position=eval(elements[1+num_of_team_str_elements+1]) )
		# print team_str
	#print dict_
	# print dict_teams
	# print dict_rankings
	fopen.close()
	dict_['teams'] = dict_teams
	dict_['rankings'] = dict_rankings
	return dict_

def get_list_of_teams_in_WC_soccerbase_format(filename1,year):
	fopen = open(filename1,'r')
	lines = fopen.readlines()
	dict_ = {}
	days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	match = 1
	teams = []
	dict_matches = {}
	is_date_str = False
	current_category = None
	for line1 in lines:
		line = line1.strip()
		#print (line.strip()).split('\t')
		for day in days:
			if ( line.find(str(year)) != -1 ):
				current_date = line.strip()
				#print current_date
				is_date_str = True
				break
			else:
				is_date_str = False
		if ( line.find('Cat') != -1 ):
			# if ( current_category != None): print current_category, "total matches of previous", match-1
			current_category = line.replace('Cat ','')
			# print current_category
			# current_
		elif ( is_date_str == True ):
			pass
		else:
			match += 1
			elements = line.split('\t')
			# print elements
			# stop_here
			dict_matches['{}'.format(match)] = dict(result=elements[1].replace(' ',''),
				category=current_category,date=current_date,
				team1=elements[0].strip(),team2=elements[2].strip())
			teams.append(elements[0].strip())
			teams.append(elements[2].strip())
	# print current_category, "total matches of previous", match-1
	print "Loaded results dict", filename1
	print "\tTotal matches  = ", match-1
	dict_['matches'] = dict_matches
	dict_['teams']   = list(set(teams))
	print "\tTotal teams = ", len(dict_['teams'])
	# print dict_matches
	# stop_here
	return dict_

def get_list_of_teams_in_2010WC():
	fopen = open('2010WC_results.txt','r')
	lines = fopen.readlines()
	dict_ = {}
	days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	match = 1
	teams = []
	dict_matches = {}
	for line1 in lines:
		line = line1.strip()
		# print (line.strip()).split('\t')
		for day in days:
			if ( line.find(day) != -1 ):
				current_category = line.split('-')[1]
				break
		# print current_category	
		if ( line.find('GMT') != - 1):
			match += 1
			elements = line.split('\t')
			dict_matches['{}'.format(match)] = dict(result=elements[3],category=current_category,
				team1=elements[1],team2=elements[2])
			teams.append(elements[1])
			teams.append(elements[2])
	dict_['matches'] = dict_matches
	dict_['teams']   = list(set(teams))
	return dict_
	#print dict_
	#print len(dict_.keys())
	# print set(teams), len(set(teams))

def analyze_result(result):
	elements = result.split('-')
	# print elements
	homegoals , awaygoals = eval(elements[0]),eval(elements[1])
	if ( homegoals > awaygoals ):
		result_string = 'home'
	elif ( homegoals == awaygoals ):
		result_string ='draw'
	else:
		result_string ='away'
	return result_string,homegoals,awaygoals

def get_number_of_points(result_str,hteam,ateam, targetteam):
	result_string,homegoals,awaygoals = analyze_result(result_str)
	if ( targetteam == hteam):
		if ( result_string == 'home'):
			return 3
		elif ( result_string == 'away'):
			return 0
		else:
			return 1
	elif ( targetteam == ateam):
		if ( result_string == 'home'):
			return 0
		elif ( result_string == 'away'):
			return 3
		else:
			return 1


def analyze_2010_WC_with_ranking():
	dict_ranking = load_dict_ranking_from_file()
	dict_ = get_list_of_teams_in_2010WC()
	for i,team in enumerate(dict_['teams']):
		# print team
		#print dict_ranking['teams'].keys()
		#break
		if team in (dict_ranking['teams'].keys()):
			print i+1,team, dict_ranking['teams'][team]['rank']
			# pass
		else:
			print team, " in 2010 WC "
			# if ( get_close_matches(team))
			print "\t", get_close_matches(team,dict_ranking['teams'].keys())
			print "\t",team,False
		predicted   = []
	won_matches         = []
	drawn_matches       = []
	rank_diffs_in_draws = []
	num_of_matches = len(dict_['matches'].keys())
	for match in dict_['matches'].keys():
		team1 = dict_['matches'][match]['team1']
		rank1 = dict_ranking['teams'][team1]['rank']
		team2 = dict_['matches'][match]['team2']
		rank2 = dict_ranking['teams'][team2]['rank']
		result = dict_['matches'][match]['result']
		print '({}) {}- ({}) {}'.format( dict_ranking['teams'][team1]['rank'],team1,
			dict_ranking['teams'][team2]['rank'],team2 )
		
		# results = 	# print results
		result_string, hg, ag  = analyze_result(result)
		if ( result_string != 'draw'):	
			won_matches.append(match)
			if ( rank1 < rank2 ):
				result_string_rank = 'home'
			elif (rank1 > rank2 ):
				result_string_rank = 'away'
			else:
				result_string_rank = 'draw'
			print '\t', result, result_string, 'prediction ', result_string_rank
			if  (result_string == result_string_rank):
				predicted.append(match)
		else:
			drawn_matches.append(match)
			rank_diffs_in_draws.append(abs(rank1-rank2))

	print "correctly predicted victories by ranking dict of 2010 WC = {}/{} = {:.2f}\%".format(len(predicted),len(won_matches),
		100.0*len(predicted)/len(won_matches))
	print "Number of draws in WC 2010 (in normal time): {}, avg rank diff = {}".format(len(drawn_matches),mean(rank_diffs_in_draws))

	quarter_teams = []
	for match in dict_['matches'].keys():
		# print dict_['matches'][match]['category']
		if (dict_['matches'][match]['category']).strip() == 'Quarterfinals':
			team1, team2 = dict_['matches'][match]['team1'],dict_['matches'][match]['team2']
			quarter_teams.append(team1)
			quarter_teams.append(team2)

	print len(quarter_teams)
	correct_ranking = []
	for team in quarter_teams:

		rank = dict_ranking['teams'][team]['rank']
		print team, rank
		if ( rank <= 8 ):
			correct_ranking.append(rank)

	print "Number of quarterfinal teams correctly predicted = {}/8={:.2f}\%".format(
			len(correct_ranking),100.*len(correct_ranking)/8.0)

def analyze_2010_WC_results_rankings():
	dict_wc_results = get_list_of_teams_in_2010WC()
	dict_ranking    = load_dict_ranking_from_file('top_60_FIFA_ranking_May_2010.txt')
	analyze_WC_results_with_ranking(dict_ranking,dict_wc_results,'2010 WC')

def analyze_2010_WC_results_rankings_mod():
	dict_wc_results = get_list_of_teams_in_2010WC()
	dict_ranking    = load_dict_ranking_from_file('top_60_FIFA_ranking_May_2010.txt')
	dict_           = get_2010_ranking_dicts_comparison() 
	# table obtained from Nate Silver analysis
	# http://espnfc.com/world-cup/columns/story/_/id/5392992/ce/us/soccer-power-index-update?cc=5901&ver=us


	dict_ranking    = dict_['SPI']
	analyze_WC_results_with_ranking(dict_ranking,dict_wc_results,'2010 WC')

def get_2010_ranking_dicts_comparison():
		fopen = open('2010_various_ranking.txt','r')
		lines= fopen.readlines()
		header = lines[0].strip()
		ranking_labels = header.split('\t')[1:]
		print ranking_labels
		fopen.close()
		dict_ = {}
		for label in ranking_labels:
			dict_[label] = {}
			dict_[label]['teams'] = {}

		for i in range(1,1+len(ranking_labels)):
			print ranking_labels[i-1]
			for line in [ line.strip() for line in lines[1:] ]:
				# print line
				elements = line.split('\t')
				# print len(elements)
				team = elements[0]
				dict_[ranking_labels[i-1]]['teams'][team] = dict(rank=eval(elements[i]))
		print dict_
		# raise ValueError, 'here'
		return dict_

def analyze_2010_WC_results_points_generated_vs_ranking():
	


	dict_wc_results = get_list_of_teams_in_2010WC()
	dict_ranking    = load_dict_ranking_from_file('top_60_FIFA_ranking_May_2010.txt')
	dict_           = get_2010_ranking_dicts_comparison() 
	# table obtained from Nate Silver analysis
	# http://espnfc.com/world-cup/columns/story/_/id/5392992/ce/us/soccer-power-index-update?cc=5901&ver=us


	dict_ranking_2    = dict_['FIFA']
	for team in dict_wc_results['teams']:
		print team, dict_ranking['teams'][team]['rank'], dict_ranking_2['teams'][team]['rank']
	colors = ['r','b','g','k','y']
	figure(1); clf()
	for color,key in zip(colors,dict_.keys()):
		dict_ranking = dict_[key]
		if ( key != 'Actual'):
			analyze_WC_results_points_vs_ranking(dict_ranking,dict_wc_results,'2010 WC {}'.format(key),
				color=color)
	# SOME ANALYSIS
	# The fifa rankings were significantly less predicted when measured by the R^2 of the resulting linear regression line
	# when calculated over points/game and rank. 
	# either of the reamining 3 ranking systems were about equal by this measure.
	# Taking the absolute best of these 3 very closely packed rankings, the SPI, would seem to suggest that
	# (in JAN 2014 ), the top seeds should be Brazil, Argentina, Spain Germany, Colombia,
	# Uruguay, Chile and France
	# i.e. so that Switzerland and Belgium would be replaced with Chile and France.
	# Need more analysis of these other rankings that I did with FIFA's official. To see if they really would have predicted 
	# the winner in more cases. The predicted favorite by the SPI ranking was actually less than FIFA. Curiously.
	# 
def analyze_2006_WC_results_rankings():
	# dict_wc_results = get_list_of_teams_in_2006WC()
	dict_wc_results = get_list_of_teams_in_WC_soccerbase_format('2006WC_results.txt',2006)
	analyze_WC_results_dict(dict_wc_results)
	# stop_here
	dict_ranking    = load_dict_ranking_from_file('top_90_FIFA_rankings_May_2006.txt')
	analyze_WC_results_with_ranking(dict_ranking,dict_wc_results,'2006 WC')

def analyze_2006_WC_results_points_generated_vs_ranking():
	# dict_wc_results = get_list_of_teams_in_2010WC()
	dict_wc_results = get_list_of_teams_in_WC_soccerbase_format('2006WC_results.txt',2006)

	dict_ranking    = load_dict_ranking_from_file('top_90_FIFA_ranking_May_2006.txt')
	analyze_WC_results_points_vs_ranking(dict_ranking,dict_wc_results,'2006 WC',color='b')

def analyze_2002_WC_results_rankings():
	dict_wc_results = get_list_of_teams_in_WC_soccerbase_format('2002WC_results.txt',2002)
	analyze_WC_results_dict(dict_wc_results)
	# stop_here
	dict_ranking    = load_dict_ranking_from_file('top_90_FIFA_ranking_May_2002.txt')
	analyze_WC_results_with_ranking(dict_ranking,dict_wc_results,'2002 WC')


def analyze_2002_WC_results_points_generated_vs_ranking():
	dict_wc_results = get_list_of_teams_in_WC_soccerbase_format('2002WC_results.txt',2002)
	analyze_WC_results_dict(dict_wc_results)
	# stop_here
	dict_ranking    = load_dict_ranking_from_file('top_90_FIFA_ranking_May_2002.txt')
	# analyze_WC_results_with_ranking(dict_ranking,dict_wc_results,'2002 WC')

	analyze_WC_results_points_vs_ranking(dict_ranking,dict_wc_results,'2002 WC',color='g')

def parse_wikipedia_team_confederation(filename1,team):
	pass

import os
def add_files_to_repo(files=['*.py','*.txt','*.csv']):
	for file1 in files:
		os.system('git add {}'.format(file1))

def push_updates_to_github():
	os.system('git push -u origin master')

def analyze_WC_results_dict(dict_):
	categories = []
	for match in dict_['matches']:
		categories.append( dict_['matches'][match]['category'])
	print len(categories)
	print set(categories)
	categories = list(set(categories))
	# cat_matches = [[]]*(len(categories))
	cat_matches = {}
	for cat in categories:
		cat_matches[cat] = []

	for match in dict_['matches']:
		# index1 = categories.index( dict_['matches'][match]['category'] )
		# print index1
		# (cat_matches[index1]).append(match)
		(cat_matches[dict_['matches'][match]['category']]).append(match)
	# print cat_matches
	# stop_here
	for i,cat in enumerate(categories):
		print '',cat, "number of matches =", len(cat_matches[cat]),''
		# for match in cat_matches[i]:
		# 	print dict_['matches'][match]['team1'],dict_['matches'][match]['result'],\
		# 		dict_['matches'][match]['team2']

	for team in dict_['teams']:
		matches_played_by_team= 0
		for match in dict_['matches']:
			if ( dict_['matches'][match]['category'] == 'Group Matches' and team in [ dict_['matches'][match]['team1'],dict_['matches'][match]['team2'] ]):	
				matches_played_by_team += 1
				# print team
		# print matches_played_by_team
		if ( matches_played_by_team != 3 ):
			raise ValueError, "Not all group matches ({}/3) loaded for {}, total matches = {}".format(
				matches_played_by_team,team,len(dict_['matches'].keys()))

def analyze_WC_results_with_ranking(dict_ranking,dict_wc_results,label_results):
	from difflib import get_close_matches
	# dict_ranking = load_dict_ranking_from_file()
	dict_  = dict_wc_results
	# dict_ = get_list_of_teams_in_2010WC()
	for i,team in enumerate(dict_['teams']):
		# print team
		#print dict_ranking['teams'].keys()
		#break
		if team in (dict_ranking['teams'].keys()):
			#print i+1,team, dict_ranking['teams'][team]['rank']
			pass
		else:
			print team, " in ", label_results
			# if ( get_close_matches(team))
			print "\t", get_close_matches(team,dict_ranking['teams'].keys())
			print "\t",team,False
	predicted   = []
	predicted_teams = []
	predicted   = []
	predicted_teams = []
	not_predicted   = []
	not_predicted_teams_results = []
	#stop_here
	won_matches = []
	drawn_matches = []
	rank_diffs_in_draws = []
	draw_info = []
	num_of_matches = len(dict_['matches'].keys())
	print "Number of matches = {}".format(num_of_matches)
	for match in dict_['matches'].keys():
		team1 = dict_['matches'][match]['team1']
		rank1 = dict_ranking['teams'][team1]['rank']
		team2 = dict_['matches'][match]['team2']
		rank2 = dict_ranking['teams'][team2]['rank']
		result = dict_['matches'][match]['result']
		print '({}) {}- ({}) {}'.format( dict_ranking['teams'][team1]['rank'],team1,
			dict_ranking['teams'][team2]['rank'],team2 )
		
		# results = 	# print results
		result_string, hg, ag  = analyze_result(result)
		if ( result_string != 'draw'):	
			won_matches.append(match)
			
			if ( rank1 < rank2 ):
				result_string_rank = 'home'
			elif (rank1 > rank2 ):
				result_string_rank = 'away'
			else:
				result_string_rank = 'draw'
			print '\t', result, result_string, 'prediction ', result_string_rank
			if  (result_string == result_string_rank):
				predicted.append(match)
				predicted_teams.append([team1,team2])
			else:
				not_predicted.append(match)
				not_predicted_teams_results.append([team1,rank1,team2,rank2,result_string,result_string_rank])
		else:
			drawn_matches.append(match)
			rank_diffs_in_draws.append(abs(rank1-rank2))
			draw_info.append( [team1,team2,rank1,rank2 ] )
	print "correctly predicted victories by ranking dict of {} = {}/{} = {:.2f}\%".format(
		label_results,len(predicted),len(won_matches),
		100.0*len(predicted)/len(won_matches))
	print "Number of draws in {} (in normal time): {}, avg rank diff = {}".format(
		label_results,len(drawn_matches),mean(rank_diffs_in_draws))
	print "\t {}".format(rank_diffs_in_draws)

	quarter_teams = []
	for match in dict_['matches'].keys():
		# print dict_['matches'][match]['category']
		if (dict_['matches'][match]['category']).strip() == 'Quarterfinals':
			team1, team2 = dict_['matches'][match]['team1'],dict_['matches'][match]['team2']
			quarter_teams.append(team1)
			quarter_teams.append(team2)

	print len(quarter_teams)
	correct_ranking = []
	for team in quarter_teams:

		rank = dict_ranking['teams'][team]['rank']
		print team, rank
		if ( rank <= 8 ):
			correct_ranking.append(rank)

	print "Number of quarterfinal teams in {} correctly predicted = {}/8={:.2f}\%".format(
			label_results,len(correct_ranking),100.*len(correct_ranking)/8.0)
	return drawn_matches,draw_info,predicted,predicted_teams,not_predicted,not_predicted_teams_results

def analyze_WC_results_points_vs_ranking(dict_ranking,dict_wc_results,label_results,color='r'):
	from difflib import get_close_matches
	# dict_ranking = load_dict_ranking_from_file()
	dict_  = dict_wc_results
	# dict_ = get_list_of_teams_in_2010WC()
	for i,team in enumerate(dict_['teams']):
		# print team
		#print dict_ranking['teams'].keys()
		#break
		if team in (dict_ranking['teams'].keys()):
			#print i+1,team, dict_ranking['teams'][team]['rank']
			pass
		else:
			print team, " in ", label_results
			# if ( get_close_matches(team))
			print "\t", get_close_matches(team,dict_ranking['teams'].keys())
			print "\t",team,False
	points_generated, prewc_ranks, points_per_game = [],[], []
	num_of_matches = len(dict_['matches'].keys())
	print "Number of matches = {}".format(num_of_matches)
	for team in dict_['teams']:
		
		Nmatches = 0
		points   = 0
		for match in dict_['matches'].keys():
			if ( team in [dict_['matches'][match]['team1'],dict_['matches'][match]['team2'] ]):
				# print match
				Nmatches += 1
				hometeam, awayteam = dict_['matches'][match]['team1'],dict_['matches'][match]['team2'] 
				result_string = dict_['matches'][match]['result']
				points += get_number_of_points(result_string,hometeam,awayteam,team)

		# print team, Nmatches, points

		rankteam = dict_ranking['teams'][team]['rank']
		points_generated.append(points)
		points_per_game.append(1.0*points/Nmatches)
		prewc_ranks.append(rankteam)
	
	figure(1)
	# clf()
	print color, label_results
	plot(prewc_ranks,points_per_game,'o',markeredgewidth=3.0,mfc='None',markeredgecolor=color)
	title("points/game generated vs pre-WC FIFA ranking")
	a,b,RR = linreg(prewc_ranks,points_generated)
	print RR

def get_delimited_str(target_str,start_str,end_str):
	ii = target_str.find(start_str)
	jj = target_str.find(end_str)
	return (target_str[ii+len(start_str):jj]).strip()

def get_confederation_membership_dict(verbose=True):
	fopen = open('all_member_nations.txt','r')
	lines = fopen.readlines()
	dict_ = {}
	dict_confed = {}
	dict_teams  = {}
	dict_annotations = {}
	for line in [ line.strip() for line in lines]:
		# print line, line.split(), line.split('\t')
		# print ""
		if ( line.find('Confederation') != -1 ):
			# print line.split('Confederation')[1], get_delimited_str(line,'(',')')
			current_continent = get_delimited_str(line,'(',')') 
			# current_confederation = 
			current_confederation = get_delimited_str(line,'Confederation ','(',)
			dict_confed[current_confederation]                = {}
			dict_confed[current_confederation]['continent']   = current_continent
			dict_confed[current_confederation]['annotations'] = []
			dict_confed[current_confederation]['teams']       = []
		elif ( line.find(':') != -1 ):
			(dict_confed[current_confederation]['annotations']).append(line)	
		else:
			current_team = line.split('\t')[0]
			# print team_target
			(dict_confed[current_confederation]['teams']).append(current_team)
			if ( len(line.split('\t')) == 1):
				dict_teams[current_team] = dict(confederation=current_confederation)
			else:
				dict_teams[current_team] = dict(confederation=current_confederation,
					annotation=line.split()[1])

	# print annotations
	fopen.close()
	if ( verbose==True ):
		N = 0
		for confed in dict_confed:
			print '\t',confed, len(dict_confed[confed]['teams'])
			N += len(dict_confed[confed]['teams'])
		print "Total teams ", N, " in dictionary: ", len(dict_teams.keys())
	dict_['confed'] = dict_confed
	dict_['teams']  = dict_teams
	return dict_

def get_confederation_membership(dict_,team_target):
	# if ( dict_ == None ):
	# 	dict_ = get_confederation_membership_dict()
	# else:
	# 	pass

	if ( team_target in (dict_['teams']).keys() ):
		team_confed = dict_['teams'][team_target]['confederation']
	else:
		matches =get_close_matches(team_target,dict_['teams'].keys() )
		if ( len(matches) == 1):
			team_confed = dict_['teams'][matches[0]]['confederation']
		elif ( len(matches) > 1 ):
			for j,match in enumerate(matches):
				print j, match,
			print ""
			i = eval(raw_input('Select match above or enter None: '))
			return dict_['teams'][matches[i]]['confederation']
		else:
			raise ValueError, "No match found for team {}".format(team_target)
	return team_confed

def test_WC_teams_for_membership(dict_membership,dict_wc_results):
	confeds = []
	for i,team in enumerate(dict_wc_results['teams']):
		confed = get_confederation_membership(dict_membership,team)
		print i+1,team,confed
		confeds.append(confed)
	
	for confed in set(confeds):
		N = 0
		for team in dict_wc_results['teams']:
			if ( get_confederation_membership(dict_membership,team) == confed ):
				N += 1
		print "Teams for ", confed, " at WC = ", N

def analyze_WC_results_by_ranking_and_confed_memberships_2010():
	dict_membership = get_confederation_membership_dict()
	# print 'testigget_confederation_membership(dict_membership,'Mexico')

	# dict_wc_results = get_list_of_teams_in_WC_soccerbase_format('2006WC_results.txt',2006)
	# dict_wc_results = get_list_of_teams_in_WC_soccerbase_format('2002WC_results.txt',2002)
	dict_wc_results = get_list_of_teams_in_2010WC()
	test_WC_teams_for_membership(dict_membership,dict_wc_results)
	dict_ranking    = load_dict_ranking_from_file('top_60_FIFA_ranking_May_2010.txt')
	resdict = analyze_WC_results_by_ranking_and_confed_memberships('2010 WC',
		dict_ranking,dict_membership,dict_wc_results)
	return resdict

def analyze_WC_results_by_ranking_and_confed_memberships_2006():
	dict_membership = get_confederation_membership_dict()
	dict_wc_results = get_list_of_teams_in_WC_soccerbase_format('2006WC_results.txt',2006)

	test_WC_teams_for_membership(dict_membership,dict_wc_results)
	dict_ranking    = load_dict_ranking_from_file('top_90_FIFA_ranking_May_2006.txt')
	resdict = analyze_WC_results_by_ranking_and_confed_memberships('2006 WC',
		dict_ranking,dict_membership,dict_wc_results)
	return resdict
	
def analyze_WC_results_by_ranking_and_confed_memberships_2002():
	dict_membership = get_confederation_membership_dict()
	dict_wc_results = get_list_of_teams_in_WC_soccerbase_format('2002WC_results.txt',2002)

	test_WC_teams_for_membership(dict_membership,dict_wc_results)
	dict_ranking    = load_dict_ranking_from_file('top_90_FIFA_ranking_May_2002.txt')
	resdict = analyze_WC_results_by_ranking_and_confed_memberships('2002 WC',
		dict_ranking,dict_membership,dict_wc_results)
	return resdict
	
def analyze_WC_results_by_ranking_and_confed_memberships(label_str,dict_ranking,dict_membership,
		dict_wc_results,intraconfederation=False):
	draws,draw_teams,pre,pre_t,not_predicted,not_predicted_teams_results = analyze_WC_results_with_ranking(
		dict_ranking,dict_wc_results,label_str)
	print "Analysis of ranking predicted results for ", label_str
	print "\t Results within same confed are not included : {}".format(intraconfederation)
	print "\t predicted wins, not predicted wins, draws",len(pre), len(not_predicted_teams_results), len(draws)
	print "\t tot matches = ",len(pre)+ len(not_predicted_teams_results)+ len(draws)

	print "Wins not predicted"
	print '\t {:15} {:3} {:15} {:3} {:10} {:10} {:12} {:7}'.format('Home','Rnk','Away','Rnk',
		'Result','Res Pred','Winning team','Confed')
	confeds_not_predicted = []
	confeds_involved_in_each_match = []
	for i,match in enumerate(not_predicted):
		# 
		info = not_predicted_teams_results[i]
		result_str = info[4]
		if ( result_str == 'home'):
			winning_team = info[0]
			losing_team  = info[2]
		else:
			winning_team = info[2]
			losing_team  = info[0]

		winning_team_confed = get_confederation_membership(dict_membership,winning_team)
		losing_team_confed  = get_confederation_membership(dict_membership,losing_team)

		if ( intraconfederation == True ):
			confeds_not_predicted.append( winning_team_confed )
			print '\t {:15} {:3} {:15} {:3} {:10} {:10} {:12} {:7}'.format(*(info+[winning_team,winning_team_confed]))
			confeds_involved_in_each_match.append( [winning_team_confed,losing_team_confed])
		else:
			if ( winning_team_confed != losing_team_confed ):
				confeds_not_predicted.append( winning_team_confed )
				print '\t {:15} {:3} {:15} {:3} {:10} {:10} {:12} {:7}'.format(*(info+[winning_team,winning_team_confed]))
				confeds_involved_in_each_match.append( [winning_team_confed,losing_team_confed])


	confeds = dict_membership['confed'].keys()
	print "Breakdown by confed"
	results_dict = {}
	results_dict[label_str] = {}
	for confed in confeds:
		print '{:10} {}'.format(confed, confeds_not_predicted.count(confed))
		results_dict[label_str][confed] = dict(number=confeds_not_predicted.count(confed),
			percent=confeds_not_predicted.count(confed)/len(confeds_not_predicted),
			total=len(confeds_not_predicted) )
	print "Total matches in sample", len(confeds_involved_in_each_match)
	for confed in confeds:
		Nmatch = 0
		for confeds in confeds_involved_in_each_match:
			if confed in confeds:
				Nmatch += 1
		print "\t Number of matches that involed {} = {}".format(confed,Nmatch)

		results_dict[label_str][confed]['matches'] = Nmatch
		# if confed in confeds_in_each_match:
			# print True
			
	return results_dict

def analysis_of_all_ranking_mispredicted_based_on_confed():
	dict_2010 = analyze_WC_results_by_ranking_and_confed_memberships_2010()
	dict_2006 = analyze_WC_results_by_ranking_and_confed_memberships_2006()
	dict_2002 = analyze_WC_results_by_ranking_and_confed_memberships_2002()
	dicts = [dict_2010,dict_2006, dict_2002]
	dict_membership = get_confederation_membership_dict(verbose=False)

	print "Want to predict probability based on confederation for ranking did not 'predict' correct results"
	confeds = dict_membership['confed'].keys()
	# print confeds
	print '{:10}'.format("Confed"),
	for dict_ in dicts:
		for key in dict_:
			print '{:>10}'.format(key[0:0+4]),
	print "| Total intraconfed matches"
	# 18+15+13
	for confed in confeds:
		# print key,
		print '{:10}'.format(confed),
		N    = 0
		Ntot = 0
		for dict_ in dicts:
			for key in dict_:
				# print key
				print '{:6}({:2})'.format(dict_[key][confed]['number'],dict_[key][confed]['total']),
				N += dict_[key][confed]['number']
			Ntot += dict_[key][confed]['matches']
		if ( Ntot != 0): print '| {:2}/{:2} - {:.0f}%'.format(N,Ntot,100.*N/Ntot),
		print ""
		
###		
### idea download all results from all world cups,
###
# plot the number of points for each confederation in terms of pts/game over time.
# should give a good indication of how things have changed over time for the confederations
# should also allow for alternate definitions of names, makes everything much easier rather than
# editing the source files
# base camps have been announced, would be beautiful if I could incorporate this to calculations
