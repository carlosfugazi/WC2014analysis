#
# analyze FIFA rankings in 2010
#
def load_dict_ranking_from_file():
	filename1 = 'top_60_FIFA_ranking_May_2010.txt'
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

def get_list_of_teams_in_2006WC():
	fopen = open('2006WC_results.txt','r')
	lines = fopen.readlines()
	dict_ = {}
	days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	match = 1
	teams = []
	dict_matches = {}
	for line1 in lines[::-1]:
		line = line1.strip()
		# print (line.strip()).split('\t')
		for day in days:
			if ( line.find(day[0:2]) != -1 ):
				current_date = line.strip()
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

def analyze_2010_WC_with_ranking():
	from difflib import get_close_matches
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
	won_matches = []
	drawn_matches = []
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
