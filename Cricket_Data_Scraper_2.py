from http.client import responses
import requests
import random


def getList(dict):
    return dict.keys()

def conditional_change(prediction, old_score, new_score):
    if new_score > old_score:
        return True
    else:
        return False

def prediction_change(prediction, old_value, new_value):
    if (new_value - old_value) == float(prediction):
        return True
    else:
        return False

#Establishing link to API

headers = {
    'X-RapidAPI-Key': "d0c522027amsh51fdd1eb86fd81fp15b046jsn5bc411c88dcc",
    'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
    }

#Link to scrape data about ongoing matches

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

response = requests.request("GET", url, headers=headers)

information = response.json()

game_types = [0] #[0] for International Games and [1] for Domestic Games

for game_type in game_types:
    data = information['typeMatches'][game_type]['seriesMatches'] 

    series_list = [] #Different ongoing Series
    match_details = [] #Different ongoing Matches

    for series_current in data:

        #Some Necessary Data Formatting and Series Finding
        try:
            curr_series_data = series_current['seriesAdWrapper']
        except:
            pass

        try:
            series_list.append([curr_series_data['seriesName'], curr_series_data['seriesId']])
            curr_series_data = curr_series_data['matches']
        except:
            pass

        if len(curr_series_data) == 0:
            curr_series_data['seriesAdWrapper'][0]['matchInfo']['matchInfo']
        
        for matchSet in curr_series_data:

            if (matchSet['matchInfo']['matchFormat'] == 'T20') and (matchSet['matchInfo']['state'] != 'Complete'):

                #Getting current Match ID

                current_match = matchSet['matchInfo']['matchId']
                match_details.append([matchSet['matchInfo']['matchId'], matchSet['matchInfo']['state']])
                
                team_1_full = [] #Batmens-Bowler Data and other Meta for Team 1
                team_2_full = [] #Batmens-Bowler Data and other Meta for Team 2

                #Batsmen Bowler Data for a Single Game

                batsmen_team_one = []
                batsmen_team_two = []
                bowlers_team_one = []
                bowlers_team_two = []

                #Meta Data for Each Team - Total Runs, Name, etc

                team_1_full.append([matchSet['matchInfo']['team1']['teamName'], matchSet['matchScore']['team1Score']])
                team_2_full.append([matchSet['matchInfo']['team2']['teamName'], matchSet['matchScore']['team2Score']])

                url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/" + str(current_match) + "/scard"

                responsetest_ = requests.request("GET", url, headers=headers)

                information_match = responsetest_.json()

                cycle_number  = 0

                #Batsmen Bowler Data for a Game

                for team_number_ID in information_match['scoreCard']:
                    for data_point in team_number_ID['batTeamDetails']['batsmenData']:
                        curr_batsmen = team_number_ID['batTeamDetails']['batsmenData'][data_point]
                        if cycle_number == 0:
                            batsmen_team_one.append([curr_batsmen['batName'], curr_batsmen['isCaptain'], curr_batsmen['isKeeper'], curr_batsmen['runs'],curr_batsmen['balls'], curr_batsmen['strikeRate'], curr_batsmen['boundaries'],curr_batsmen['sixers'], curr_batsmen['wicketCode'], curr_batsmen['bowlerId'], curr_batsmen['fielderId1'], curr_batsmen['outDesc']])
                        else:
                            batsmen_team_two.append([curr_batsmen['batName'], curr_batsmen['isCaptain'], curr_batsmen['isKeeper'], curr_batsmen['runs'],curr_batsmen['balls'], curr_batsmen['strikeRate'], curr_batsmen['boundaries'],curr_batsmen['sixers'], curr_batsmen['wicketCode'], curr_batsmen['bowlerId'], curr_batsmen['fielderId1'], curr_batsmen['outDesc']])

                    for data_point in team_number_ID['bowlTeamDetails']['bowlersData']:
                        curr_bowler = team_number_ID['bowlTeamDetails']['bowlersData'][data_point]

                        if cycle_number == 0:
                            bowlers_team_two.append([curr_bowler['bowlName'], curr_bowler['isCaptain'], curr_bowler['isKeeper'], curr_bowler['overs'], curr_bowler['maidens'], curr_bowler['runs'], curr_bowler['wickets'], curr_bowler['economy'], curr_bowler['no_balls'], curr_bowler['wides']])
                        else:
                            bowlers_team_one.append([curr_bowler['bowlName'], curr_bowler['isCaptain'], curr_bowler['isKeeper'], curr_bowler['overs'], curr_bowler['maidens'], curr_bowler['runs'], curr_bowler['wickets'], curr_bowler['economy'], curr_bowler['no_balls'], curr_bowler['wides']])

                    cycle_number += 1

                team_1_full.append(batsmen_team_one)
                team_2_full.append(batsmen_team_two)
                team_1_full.append(bowlers_team_one)
                team_2_full.append(bowlers_team_two)
            else:
                pass


team_currently_batting = team_1_full
team_currently_bowling = team_2_full

if (len(team_2_full[1]) != 0):
    team_currently_batting = team_2_full
    team_currently_bowling = team_1_full

team_batting = team_currently_batting[0][0]
batsmen_1 = 'None'
batsmen_2 = 'None'
batsmen_1_runs = 0
batsmen_2_runs = 0
batsmen_1_balls = 0
batsmen_1_sr = 0
batsmen_2_sr = 0
batsmen_2_balls = 0
batsmen_1_sixes = 0
batsmen_2_sixes = 0
batsmen_1_fours = 0
batsmen_2_fours = 0

team_bowling = team_currently_bowling[0][0]
bowler_name = 'None'
bowler_overs = 0
bowler_runs = 0
bowler_wickets = 0
bowler_maidens = 0
bowler_econ = 0
bowler_no_ball = 0
bowler_wides = 0

count_batter = 0 

team_batting_stats = team_currently_batting[0][1]['inngs1']

team_batting_runs = team_batting_stats['runs']
team_batting_overs = team_batting_stats['overs']

try:
    team_batting_wickets = team_batting_stats['wickets']
except:
    team_batting_wickets = 0 


for batter in team_currently_batting[1]:

    if count_batter == 2:
        break

    if (batter[-1] == 'batting') and (batsmen_1 == 'None') and (count_batter == 0):
        batsmen_1 = str(batter[0])
        batsmen_1_runs = int(batter[3])
        batsmen_1_balls = int(batter[4])
        batsmen_1_sr = float(batter[5])
        batsmen_1_fours = int(batter[6])
        batsmen_1_sixes = int(batter[7])
        count_batter += 1

    elif (batter[-1] == 'batting') and (batsmen_2 == 'None') and (count_batter == 1):
        batsmen_2 = str(batter[0])
        batsmen_2_runs = int(batter[3])
        batsmen_2_balls = int(batter[4])
        batsmen_2_sr = float(batter[5])
        batsmen_2_fours = int(batter[6])
        batsmen_2_sixes = int(batter[7])
        count_batter += 1

for bowler in team_currently_bowling[2]:

    if (float(bowler[3]) % 1) != 0:
        bowler_name = str(bowler[0])
        bowler_overs = float(bowler[3])
        bowler_runs = int(bowler[5])
        bowler_wickets = int(bowler[6])
        bowler_maidens = int(bowler[4])
        bowler_econ = float(bowler[7])
        bowler_no_ball = int(bowler[8])
        bowler_wides = int(bowler[9])
        break

if (43 < batsmen_1_runs < 47):
    batsmen = batsmen_1
elif (43 < batsmen_2_runs < 47):
    batsmen = batsmen_2
else:
    batsmen = 'None'

wicket_number = team_batting_wickets + 1
target_runs = int(team_batting_runs) + 60
off_balls = bowler_no_ball + bowler_wides

questions_general = ['How will the strike rate of {} of {} change in the next over'.format(batsmen_1, batsmen_1_sr),'How many fours will batsman {} hit in the next over?'.format(batsmen_2), 'How many sixes will batsman {} hit in the next over?'.format(batsmen_1), 'How many wides will bowler {} bowl in his next over?'.format(bowler), 'Will {} take a wicket in the over'.format(bowler), 'Currently bowled {} wides, will {} bowl another one this over?'.format(off_balls, bowler), 'Currently bowled {} maidens, will {} bowl another one this over?'.format(bowler_maidens, bowler), 'How will the economy of {} of {} change in the next over'.format(bowler, bowler_econ)]

questions_general_overs = ['How many runs will team {} make in the next 5 overs?'.format(team_batting), 'How many fours will batsmen {} hit in the next 5 overs'.format(batsmen_2), 'How many wickets will {} take in the next five overs'.format(bowler_name), 'Will team {} lose its {} wicket in the next five overs'.format(team_batting, wicket_number), 'Will team {} cross {} in the next 5 overs'.format(team_batting, target_runs)]

special_questions = ['Will team {} cross 50 runs in the next over?'.format(team_batting), 'Will team {} cross 100 runs in the next over?'.format(team_batting), 'Will {} score a half centuary in the next over?'.format(batsmen), 'Will {} score a centuary in the next over?'.format(batsmen), 'How many runs will the next partnership between batsman {} and {} be?'.format(batsmen_1, batsmen_2)]

if team_batting_overs < 15:
    question = [*questions_general, *questions_general_overs]
else:
    question = questions_general

question_number = random.randint(0, len(question))
question = question[question_number]

special_question = 0

if 40 < team_batting_runs < 45:
    question = special_questions[0]
    special_question = 1
elif 90 < team_batting_runs < 95:
    question = special_questions[1]
    special_question = 2
elif (43 < batsmen_1_runs < 47) or (43 < batsmen_2_runs < 47):
    question = special_questions[2]
    special_question = 3
elif (93 < batsmen_1_runs < 96) or (93 < batsmen_2_runs < 96):
    question = special_questions[3]
    special_question = 4

print(question)



prediction = input("Enter Your Desired Choice")

values_stored = str(team_batting_overs)

if (special_question == 1):
    values_stored = values_stored + str(" ") + str(team_batting_runs) 
elif (special_question == 2):
    values_stored = values_stored + str(" ") + str(team_batting_runs) 
elif (special_question == 3):
    if batsmen == 'batsmen_1':
        values_stored = values_stored + str(" ") + str(batsmen_1_runs)
    else:
        values_stored = values_stored + str(" ") + str(batsmen_2_runs)
elif (special_question == 4):
    if batsmen == 'batsmen_1':
        values_stored = values_stored + str(" ") + str(batsmen_1_runs)
    else:
        values_stored = values_stored + str(" ") + str(batsmen_2_runs)
elif (question_number == 0):
    values_stored = values_stored + str(" ") + str(batsmen_1_sr) 
elif (question_number == 1):
    values_stored = values_stored + str(" ") + str(batsmen_2_fours) 
elif (question_number == 2):
    values_stored = values_stored + str(" ") + str(batsmen_1_sixes) 
elif (question_number == 3):
    values_stored = values_stored + str(" ") + str(bowler_wides) 
elif (question_number == 4):
    values_stored = values_stored + str(" ") + str(bowler_wickets)
elif (question_number == 5):
    values_stored = values_stored + str(" ") + str(off_balls)
elif (question_number == 6):
    values_stored = values_stored + str(" ") + str(bowler_maidens)
elif (question_number == 7):
    values_stored = values_stored + str(" ") + str(bowler_econ)  
elif (question_number == 8):
    values_stored = values_stored + str(" ") + str(team_batting_runs) 
elif (question_number == 9):
    values_stored = values_stored + str(" ") + str(batsmen_2_runs) 
elif (question_number == 10):
    values_stored = values_stored + str(" ") + str(bowler_wickets) 
elif (question_number == 11):
    values_stored = values_stored + str(" ") + str(team_batting_wickets)
elif (question_number == 12):
    values_stored = values_stored + str(" ") + str(target_runs)

file = open('Test.txt', 'a')

if 0 <= question_number <= 4:
    data = '{}'.format(prediction) + str(" ") + values_stored + str('\n')
elif 5 <= question_number <= 8:
    data = '{}'.format(prediction) + str(" ") + values_stored+ str(" ") + str("5") + str(" ") + str('\n')
else:
    data = '{}'.format(prediction) + str(" ") + values_stored+ str(" ") + str("s") + str(" ") + str('\n')

file.write(data)
file.close()


file = open('Test.txt', 'r')

info_file = file.strip().readlines()

for element in info_file:
    info_file_splitted = info_file.split(" ")
    if 

question_needed = False

if (info_file_splitted[-1] == 'high'):
    if (float(team_batting_overs) - float(info_file_splitted[0])  == 5):
        question_needed = True
elif (float(team_batting_overs) - float(info_file_splitted[0]) == 1):
    question_needed = True

file.close()


if (question_needed == True):
    if (special_question == 1):
        conditional_change(prediction, info_file_splitted[1], team_batting_runs)
    elif (special_question == 2):
        conditional_change(prediction, info_file_splitted[1], team_batting_runs)
    elif (special_question == 3):
        if batsmen == 'batsmen_1':
            batsmen_stored = batsmen_1_runs
        else:
            batsmen_stored = batsmen_2_runs
        conditional_change(prediction, info_file_splitted[1], batsmen_stored)
    elif (special_question == 4):
        if batsmen == 'batsmen_1':
            batsmen_stored = batsmen_1_runs
        else:
            batsmen_stored = batsmen_2_runs
        conditional_change(prediction, info_file_splitted[1], batsmen_stored)
    elif (question_number == 0):
        conditional_change(prediction, info_file_splitted[1], batsmen_1_sr)
    elif (question_number == 1):
        prediction_change(prediction, info_file_splitted[1], batsmen_1_fours)
    elif (question_number == 2):
        prediction_change(prediction, info_file_splitted[1], batsmen_1_sixes)
    elif (question_number == 3):
        prediction_change(prediction, info_file_splitted[1], bowler_wides)
    elif (question_number == 4):
        prediction_change(prediction, info_file_splitted[1], bowler_wickets)
    elif (question_number == 5):
        prediction_change(prediction, info_file_splitted[1], team_batting_runs)
    elif (question_number == 6):
        prediction_change(prediction, info_file_splitted[1], batsmen_2_runs)
    elif (question_number == 7):
        prediction_change(prediction, info_file_splitted[1], bowler_wickets)
    elif (question_number == 8):
        conditional_change(prediction, info_file_splitted[1], team_batting_wickets)
    
    file = open('Test.txt', 'w')
    file.close()




