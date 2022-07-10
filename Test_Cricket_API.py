from http.client import responses
import requests

def getList(dict):
    return dict.keys()

#Establishing link to API

headers = {
	"X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
	"X-RapidAPI-Key": "6dc8a9fa2dmshd76336d1779068ap174c41jsn3a631cdb3743"
} 

#Link to scrape data about ongoing matches

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

response = requests.request("GET", url, headers=headers)

information = response.json()

game_types = [0, 1] #[0] for International Games and [1] for Domestic Games

for game_type in game_types:
    try:
        data = information['typeMatches'][game_type]['seriesMatches'] 

        series_list = [] #Different ongoing Series
        match_details = [] #Different ongoing Matches

        for series_current in data:
            try:
                #Some Necessary Data Formatting and Series Finding

                curr_series_data = series_current['seriesAdWrapper']
                series_list.append([curr_series_data['seriesName'], curr_series_data['seriesId']])
                curr_series_data = curr_series_data['matches']

                if len(curr_series_data) == 0:
                    curr_series_data['seriesAdWrapper'][0]['matchInfo']['matchInfo']
                
                try:
                    for matchSet in curr_series_data:

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

                        try:
                            team_1_full.append([matchSet['matchInfo']['team1']['teamName'], matchSet['matchScore']['team1Score']])
                        except:
                            pass
                        
                        try:
                            team_2_full.append([matchSet['matchInfo']['team2']['teamName'], matchSet['matchScore']['team2Score']])
                        except:
                            pass

                        url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/" + str(current_match) + "/scard"
                        print(url)

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
                                    bowlers_team_one.append([curr_bowler['bowlName'], curr_bowler['isCaptain'], curr_bowler['isKeeper'], curr_bowler['overs'], curr_bowler['maidens'], curr_bowler['runs'], curr_bowler['wickets'], curr_bowler['economy'], curr_bowler['no_balls'], curr_bowler['wides']])
                                else:
                                    bowlers_team_two.append([curr_bowler['bowlName'], curr_bowler['isCaptain'], curr_bowler['isKeeper'], curr_bowler['overs'], curr_bowler['maidens'], curr_bowler['runs'], curr_bowler['wickets'], curr_bowler['economy'], curr_bowler['no_balls'], curr_bowler['wides']])

                            cycle_number += 1

                        team_1_full.append(batsmen_team_one)
                        team_2_full.append(batsmen_team_two)
                        team_1_full.append(bowlers_team_one)
                        team_2_full.append(bowlers_team_two)

                except:
                    pass
            except:
                pass
    except:
        pass