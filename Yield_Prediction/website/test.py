import requests

headers = {
    'X-RapidAPI-Key': "6dc8a9fa2dmshd76336d1779068ap174c41jsn3a631cdb3743",
    'X-RapidAPI-Host': "cricbuzz-cricket.p.rapidapi.com"
    }

seriesName_upcoming_new = []
start_times_new = []
match_status_new = []
match_details_arr_new = []
match_ID_new = []

team_1_data = []
team_2_data = []

#Link to scrape data about ongoing matches

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
response = requests.request("GET", url, headers=headers)
information = response.json()

game_types = [0, 1, 2]
try:
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
                storage = curr_series_data['seriesName']
                curr_series_data = curr_series_data['matches']
            except:
                pass
            
            for matchSet in curr_series_data:
                if (matchSet['matchInfo']['matchFormat'] == 'T20') and (matchSet['matchInfo']['state'] != 'Complete'):
                    seriesName_upcoming_new.append(storage)
                    match_status_new.append('Live')
                    match_details_fire = matchSet['matchInfo']['team1']['teamName'] + str(" ") + str("vs") + str(" ") + matchSet['matchInfo']['team2']['teamName']
                    match_details_arr_new.append(match_details_fire)
                    #Getting current Match ID

                    match_ID_new.append(int(matchSet['matchInfo']['matchId']))

                    a = matchSet['matchScore']['team1Score']

                    try:
                        b = matchSet['matchScore']['team2Score']
                    except:
                        b = {}


                    team_1_data.append([matchSet['matchInfo']['team1']['teamName'], a])
                    team_2_data.append([matchSet['matchInfo']['team2']['teamName'], b])
                    print(team_1_data)
                    print(team_2_data)


except:
    pass
